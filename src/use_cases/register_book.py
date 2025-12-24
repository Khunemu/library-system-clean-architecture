from domain.models.book import Book, Isbn

class RegisterBookUseCase:
    def __init__(self, repository, ai_service):
        self.repository = repository
        self.ai_service = ai_service

    def execute(self, isbn_value: str, title: str):
        isbn = Isbn(isbn_value)
        if self.repository.find_by_isbn(isbn):
            raise ValueError("このISBNは既に登録されています")
        
        description = self.ai_service.generate_description(title)
        new_book = Book(isbn, title)
        self.repository.save(new_book)
        return new_book, description
