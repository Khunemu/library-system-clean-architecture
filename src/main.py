import uvicorn
from fastapi import FastAPI
from infrastructure.db.memory_book_repository import MemoryBookRepository
from use_cases.register_book import RegisterBookUseCase
from interfaces.api.book_controller import create_book_router

# --- 1. 全軍の配備（依存性の注入） ---
# 倉庫を用意し、作戦官を任命し、受付窓口に配属する
repository = MemoryBookRepository()
register_use_case = RegisterBookUseCase(repository)
book_router = create_book_router(register_use_case)

# --- 2. 城郭（FastAPI）の起動 ---
app = FastAPI(title="図書館要塞 API")
app.include_router(book_router)

@app.get("/")
def read_root():
    return {"message": "図書館要塞は正常に稼働中である。"}

if __name__ == "__main__":
    # 港（ポート）8000番で待機せよ
    uvicorn.run(app, host="0.0.0.0", port=8000)
