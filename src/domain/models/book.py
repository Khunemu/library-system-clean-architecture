from dataclasses import dataclass

@dataclass(frozen=True)
class Isbn:
    value: str
    def __post_init__(self):
        if not self.value:
            raise ValueError("ISBNは必須です")

@dataclass
class Book:
    isbn: Isbn
    title: str
    def __post_init__(self):
        if not self.title:
            raise ValueError("本のタイトルは必須です")
