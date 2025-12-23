from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from use_cases.register_book import RegisterBookUseCase

# 1. 外部から届く「電文（リクエスト）」の形を定義
class RegisterBookRequest(BaseModel):
    isbn: str
    title: str

# 2. 受付窓口（ルーター）の設置
router = APIRouter()

# この窓口を動かすには「作戦官」が必要。後で合流させる。
def create_book_router(register_use_case: RegisterBookUseCase):
    
    @router.post("/books")
    async def register_book(request: RegisterBookRequest):
        try:
            # 届いた電文を作戦官に渡し、作戦を実行させる
            book = register_use_case.execute(request.isbn, request.title)
            return {"status": "success", "book": {"isbn": book.isbn.value, "title": book.title}}
        except ValueError as e:
            # 作戦官が「軍律違反」を報告してきたら、外部にも警告を出す
            raise HTTPException(status_code=400, detail=str(e))
            
    return router
