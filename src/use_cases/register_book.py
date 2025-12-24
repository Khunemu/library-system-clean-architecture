from domain.models.book import Book, Isbn

class RegisterBookUseCase:
    def __init__(self, repository, ai_service):
        self.repository = repository
        self.ai_service = ai_service

    def execute(self, isbn_value: str, title: str):
        isbn = Isbn(isbn_value)
        
        # 既に登録されているか確認
        if self.repository.find_by_isbn(isbn):
            raise ValueError(f"ISBN {isbn_value} は既に登録されています")

        # AIに紹介文を書かせる
        description = self.ai_service.generate_description(title)
        
        # 【重要】紹介文(description)をしっかりBookに込める！
        new_book = Book(isbn, title, description)
        
        # 石板に保存（今度は紹介文も一緒に保存されます）
        self.repository.save(new_book)
        
        return new_book, description
