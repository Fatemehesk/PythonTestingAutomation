# models.py
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class BookStatus:
    AVAILABLE = "Available"
    BORROWED = "Borrowed"

class Book:
    def __init__(self, title: str, author: str, isbn: str, genre: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.status = BookStatus.AVAILABLE
        self.borrowed_by = None
        self.due_date = None

    def borrow(self, member_id: str, borrow_days: int = 14):
        if self.status == BookStatus.BORROWED:
            raise Exception("Book is already borrowed.")
        self.status = BookStatus.BORROWED
        self.borrowed_by = member_id
        self.due_date = datetime.now() + timedelta(days=borrow_days)

    def return_book(self):
        if self.status == BookStatus.AVAILABLE:
            raise Exception("Book is not borrowed.")
        self.status = BookStatus.AVAILABLE
        self.borrowed_by = None
        self.due_date = None

class MembershipType:
    STANDARD = "Standard"
    PREMIUM = "Premium"

class Member:
    def __init__(self, name: str, member_id: str, membership_type: str = MembershipType.STANDARD):
        self.name = name
        self.member_id = member_id
        self.membership_type = membership_type
        self.borrowed_books = []
        self.fines = 0.0

    def can_borrow(self):
        max_books = 5 if self.membership_type == MembershipType.PREMIUM else 2
        return len(self.borrowed_books) < max_books and self.fines == 0.0

    def borrow_book(self, book: Book):
        if not self.can_borrow():
            raise Exception("Cannot borrow more books or outstanding fines exist.")
        book.borrow(self.member_id)
        self.borrowed_books.append(book)

    def return_book(self, book: Book, days_late: int, fine_per_day: float):
        book.return_book()
        self.borrowed_books.remove(book)
        if days_late > 0:
            self.fines += days_late * fine_per_day
