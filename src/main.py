import uvicorn
from fastapi import FastAPI
from infrastructure.db.memory_book_repository import MemoryBookRepository
from infrastructure.ai.gemini_service import GeminiService
from use_cases.register_book import RegisterBookUseCase
from interfaces.api.book_controller import create_book_router

# 1. 配備
repository = MemoryBookRepository()
# 閣下のキーを直接埋め込み（二度と404や401に悩まされないために）
# src/main.py の中盤を以下のように修正
api_key = os.getenv("GEMINI_API_KEY")
ai_service = GeminiService(api_key=api_key)
register_use_case = RegisterBookUseCase(repository, ai_service)
book_router = create_book_router(register_use_case)

# 2. 起動
app = FastAPI(title="AI図書館要塞・最終版")
app.include_router(book_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
