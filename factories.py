# factories.py
from models import Book
from abc import ABC, abstractmethod

class IBookFactory(ABC):
    @abstractmethod
    def create_book(self, title: str, author: str, isbn: str, genre: str) -> Book:
        pass

class BookFactory(IBookFactory):
    def create_book(self, title: str, author: str, isbn: str, genre: str) -> Book:
        return Book(title, author, isbn, genre)
