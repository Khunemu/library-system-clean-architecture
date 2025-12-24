# 必要な部品をインストール
pip install python-dotenv

# main.py を修正
cat <<EOF > src/main.py
import uvicorn
import os
from fastapi import FastAPI
from dotenv import load_dotenv  # 追加
from infrastructure.db.sqlite_book_repository import SqliteBookRepository
from infrastructure.ai.gemini_service import GeminiService
from use_cases.register_book import RegisterBookUseCase
from interfaces.api.book_controller import create_book_router

# .envファイルから環境変数を読み込む
load_dotenv()

repository = SqliteBookRepository("library.db")

# 環境変数からキーを取得（コードには直接書かない）
api_key = os.getenv("GEMINI_API_KEY")
ai_service = GeminiService(api_key=api_key)

register_use_case = RegisterBookUseCase(repository, ai_service)
book_router = create_book_router(register_use_case, repository)

app = FastAPI(title="不滅のAI図書館要塞")
app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
