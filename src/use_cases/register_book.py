from domain.models.book import Book, Isbn
from domain.repositories.book_repository import BookRepository

class RegisterBookUseCase:
    """
    『新刊登録作戦』を指揮する担当官。
    """
    def __init__(self, repository: BookRepository):
        # どの倉庫（リポジトリ）を使うかは、着任時に指示される
        self.repository = repository

    def execute(self, isbn_str: str, title: str) -> Book:
        """
        作戦実行：新しい本を登録する
        """
        isbn = Isbn(isbn_str)
        
        # 重複チェック：既に同じISBNの本が倉庫にないか確認
        existing_book = self.repository.find_by_isbn(isbn)
        if existing_book:
            raise ValueError(f"作戦失敗：ISBN {isbn_str} は既に登録済みです（『{existing_book.title}』）")

        # 新しい兵士（本）を作成
        new_book = Book(isbn=isbn, title=title)
        
        # 倉庫に収容
        self.repository.save(new_book)
        
        return new_book
