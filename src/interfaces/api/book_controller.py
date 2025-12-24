from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class RegisterBookRequest(BaseModel):
    isbn: str
    title: str

router = APIRouter()

def create_book_router(register_use_case, repository): # repositoryを引数に追加
    @router.post("/books")
    async def register_book(request: RegisterBookRequest):
        try:
            book, desc = register_use_case.execute(request.isbn, request.title)
            return {
                "status": "success",
                "book": {"isbn": book.isbn.value, "title": book.title, "description": desc}
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # 【新設】本の一覧を返す窓口
    @router.get("/books")
    async def list_books():
        books = repository.find_all()
        return [{"isbn": b.isbn.value, "title": b.title, "description": b.description} for b in books]

    return router
