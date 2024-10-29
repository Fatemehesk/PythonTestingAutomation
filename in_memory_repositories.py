# in_memory_repositories.py
from typing import List, Optional
from models import Book, Member
from repositories import IBookRepository, IMemberRepository

class InMemoryBookRepository(IBookRepository):
    def __init__(self):
        self.books = {}

    def add_book(self, book: Book):
        self.books[book.isbn] = book

    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.books.get(isbn, None)

    def list_available_books(self) -> List[Book]:
        return [book for book in self.books.values() if book.status == BookStatus.AVAILABLE]

class InMemoryMemberRepository(IMemberRepository):
    def __init__(self):
        self.members = {}

    def add_member(self, member: Member):
        self.members[member.member_id] = member

    def get_member_by_id(self, member_id: str) -> Optional[Member]:
        return self.members.get(member_id, None)
