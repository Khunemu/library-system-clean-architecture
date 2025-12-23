import sqlite3

conn = sqlite3.connect('memo.db')
cursor = conn.cursor()

# 既存のテーブルを一度リセットする（※データは全部消えます！）
cursor.execute("DROP TABLE IF EXISTS memos")
cursor.execute("DROP TABLE IF EXISTS users")

# 1. ユーザー管理用のテーブル（隊員名簿）
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

# 2. メモ用のテーブル（誰が書いたか 'user_id' を記録するように進化）
cursor.execute("""
    CREATE TABLE memos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")

print("データベースの再構築（セキュリティ強化版）が完了しました！")

conn.commit()
conn.close()
