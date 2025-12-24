import sqlite3
from domain.models.book import Book, Isbn

class SqliteBookRepository:
    def __init__(self, db_path: str = "library.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    isbn TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT
                )
            """)

    def save(self, book: Book):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO books (isbn, title, description) VALUES (?, ?, ?)",
                (book.isbn.value, book.title, book.description)
            )

    def find_by_isbn(self, isbn: Isbn):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT isbn, title, description FROM books WHERE isbn = ?", (isbn.value,))
            row = cursor.fetchone()
            if row:
                return Book(Isbn(row[0]), row[1], row[2])
        return None

    # 【新設】石板から全ての記録を読み出す
    def find_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT isbn, title, description FROM books")
            return [Book(Isbn(row[0]), row[1], row[2]) for row in cursor.fetchall()]
