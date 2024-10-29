# services.py
from typing import Optional
from models import Book, Member
from repositories import IBookRepository, IMemberRepository
from notifications import NotificationService
from datetime import datetime

class BorrowService:
    def __init__(self, book_repo: IBookRepository, member_repo: IMemberRepository, notification_service: NotificationService, fine_per_day: float = 1.0):
        self.book_repo = book_repo
        self.member_repo = member_repo
        self.notification_service = notification_service
        self.fine_per_day = fine_per_day

    def borrow_book(self, member_id: str, isbn: str):
        member = self.member_repo.get_member_by_id(member_id)
        if not member:
            raise Exception("Member not found.")

        book = self.book_repo.get_book_by_isbn(isbn)
        if not book:
            raise Exception("Book not found.")

        member.borrow_book(book)
        self.notification_service.notify(f"Dear {member.name}, you have borrowed '{book.title}'. It is due on {book.due_date.strftime('%Y-%m-%d')}.")

    def return_book(self, member_id: str, isbn: str, return_date: datetime):
        member = self.member_repo.get_member_by_id(member_id)
        if not member:
            raise Exception("Member not found.")

        book = self.book_repo.get_book_by_isbn(isbn)
        if not book:
            raise Exception("Book not found.")

        if book not in member.borrowed_books:
            raise Exception("This book was not borrowed by the member.")

        days_overdue = (return_date - book.due_date).days
        member.return_book(book, days_overdue if days_overdue > 0 else 0, self.fine_per_day)

        if days_overdue > 0:
            self.notification_service.notify(f"Dear {member.name}, you have returned '{book.title}' {days_overdue} days late. Your fine is ${days_overdue * self.fine_per_day}.")

        self.notification_service.notify(f"Dear {member.name}, you have successfully returned '{book.title}'.")

class NotificationScheduler:
    def __init__(self, member_repo: IMemberRepository, book_repo: IBookRepository, notification_service: NotificationService):
        self.member_repo = member_repo
        self.book_repo = book_repo
        self.notification_service = notification_service

    def check_due_dates(self):
        for member in self.member_repo.members.values():
            for book in member.borrowed_books:
                days_left = (book.due_date - datetime.now()).days
                if days_left == 3:
                    self.notification_service.notify(f"Dear {member.name}, your book '{book.title}' is due in 3 days.")
                elif days_left < 0:
                    self.notification_service.notify(f"Dear {member.name}, your book '{book.title}' is overdue by {-days_left} days. Please return it as soon as possible.")
