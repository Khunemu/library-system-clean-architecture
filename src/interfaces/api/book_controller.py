from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class RegisterBookRequest(BaseModel):
    isbn: str
    title: str

router = APIRouter()

def create_book_router(register_use_case):
    @router.post("/books")
    async def register_book(request: RegisterBookRequest):
        try:
            book, desc = register_use_case.execute(request.isbn, request.title)
            return {
                "status": "success",
                "book": {"isbn": book.isbn.value, "title": book.title},
                "ai_description": desc
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"予期せぬエラー: {str(e)}")
    return router
