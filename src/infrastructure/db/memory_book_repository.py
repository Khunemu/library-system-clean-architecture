from typing import Dict, List, Optional
from domain.models.book import Book, Isbn
from domain.repositories.book_repository import BookRepository

class MemoryBookRepository(BookRepository):
    """
    メモリ上にデータを保持する仮設倉庫。
    DB（Render等）がなくても、これで開発を続行できる。
    """
    def __init__(self):
        # 辞書形式で本を保管する（キーはISBNの値）
        self._books: Dict[str, Book] = {}

    def save(self, book: Book) -> None:
        self._books[book.isbn.value] = book
        print(f"【兵站報告】倉庫に『{book.title}』を納めました。")

    def find_by_isbn(self, isbn: Isbn) -> Optional[Book]:
        return self._books.get(isbn.value)

    def find_all(self) -> List[Book]:
        return list(self._books.values())
