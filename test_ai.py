import os
import google.generativeai as genai

# 環境変数からキーを読み込む
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("❌ エラー: APIキーが見つかりません。exportコマンドを実行しましたか？")
    exit()

# Geminiの設定
genai.configure(api_key=api_key)

# ★ここを修正: 最新の主力モデルを指定
model_name = 'gemini-2.5-flash' 
# もしエラーが出る場合は 'models/gemini-2.5-flash' としてください

print(f"🤖 最新鋭モデル {model_name} に接続中...")
model = genai.GenerativeModel(model_name)

# AIへの質問
try:
    response = model.generate_content("総統閣下に対して、忠誠を誓う短い挨拶をしてください。")
    print("\n=== AIからの回答 ===")
    print(response.text)
    print("====================")
except Exception as e:
    print(f"❌ エラーが発生しました: {e}")
