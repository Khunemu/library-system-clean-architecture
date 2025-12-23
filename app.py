
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai

# --- 設定 ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'khunemu-secret-key-999' # 本番では環境変数推奨
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///khunemu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- データベースとログインマネージャの初期化 ---
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Gemini API設定 ---
# 開発環境と本番環境(Render)の両方に対応
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- データベースモデル ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False) # 'user' or 'ai'
    content = db.Column(db.Text, nullable=False)

# --- ログイン管理用ローダー ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- DB自動構築 (アプリ起動前) ---
with app.app_context():
    db.create_all()

# --- ルーティング ---

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('COMMANDER LOGGED IN. WELCOME BACK.', 'success')
            return redirect(url_for('chat'))
        else:
            flash('ACCESS DENIED. INVALID CREDENTIALS.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('USERNAME ALREADY EXISTS.', 'error')
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('REGISTRATION COMPLETE. PLEASE LOGIN.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        
        # 1. ユーザーメッセージ保存
        db.session.add(Message(user_id=current_user.id, role='user', content=user_input))
        db.session.commit()

        # 2. AI応答生成
        ai_reply = "API_KEY_MISSING: Set GEMINI_API_KEY environment variable."
        if GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash') # または gemini-1.5-flash
                # 簡易的な履歴コンテキストを作成（直近数件を含めることも可能だが今回はシンプルに）
                response = model.generate_content(user_input)
                ai_reply = response.text
            except Exception as e:
                ai_reply = f"SYSTEM_ERROR: {str(e)}"
        
        # 3. AIメッセージ保存
        db.session.add(Message(user_id=current_user.id, role='ai', content=ai_reply))
        db.session.commit()

        return jsonify({'response': ai_reply})

    # GET: 履歴を表示
    history = Message.query.filter_by(user_id=current_user.id).all()
    return render_template('chat.html', history=history)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('LOGGED OUT. SESSION TERMINATED.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
