# repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from models import Book, Member

class IBookRepository(ABC):
    @abstractmethod
    def add_book(self, book: Book):
        pass

    @abstractmethod
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        pass

    @abstractmethod
    def list_available_books(self) -> List[Book]:
        pass

class IMemberRepository(ABC):
    @abstractmethod
    def add_member(self, member: Member):
        pass

    @abstractmethod
    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        pass
