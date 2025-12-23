from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.book import Book, Isbn

class BookRepository(ABC):
    @abstractmethod
    def save(self, book: Book) -> None:
        pass
    @abstractmethod
    def find_by_isbn(self, isbn: Isbn) -> Optional[Book]:
        pass
    @abstractmethod
    def find_all(self) -> List[Book]:
        pass
