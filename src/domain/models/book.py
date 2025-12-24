class Isbn:
    def __init__(self, value: str):
        if not value:
            raise ValueError("ISBNは必須です")
        self.value = value

class Book:
    def __init__(self, isbn: Isbn, title: str, description: str = ""):
        self.isbn = isbn
        self.title = title
        self.description = description  # 紹介文を追加！
