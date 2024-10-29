# tests/test_services.py
import unittest
from in_memory_repositories import InMemoryBookRepository, InMemoryMemberRepository
from factories import BookFactory
from services import BorrowService
from notifications import NotificationService
from utils import EmailService
from models import MembershipType,Member
from datetime import datetime, timedelta

class MockObserver:
    def __init__(self):
        self.messages = []

    def update(self, message: str):
        self.messages.append(message)

class TestBorrowService(unittest.TestCase):
    def setUp(self):
        # Setup repositories
        self.book_repo = InMemoryBookRepository()
        self.member_repo = InMemoryMemberRepository()

        # Setup factory and create a book
        self.book_factory = BookFactory()
        self.book = self.book_factory.create_book("The Great Gatsby", "F. Scott Fitzgerald", "1112223334", "Novel")
        self.book_repo.add_book(self.book)

        # Create a member
        self.member = Member("Charlie", "M003", MembershipType.STANDARD)
        self.member_repo.add_member(self.member)

        # Setup notifications
        self.notification_service = NotificationService()
        self.mock_observer = MockObserver()
        self.notification_service.attach(self.mock_observer)

        # Setup BorrowService
        self.borrow_service = BorrowService(self.book_repo, self.member_repo, self.notification_service, fine_per_day=2.0)

    def test_borrow_book_success(self):
        self.borrow_service.borrow_book("M003", "1112223334")
        self.assertEqual(self.book.status, BookStatus.BORROWED)
        self.assertIn(self.book, self.member.borrowed_books)
        self.assertEqual(len(self.mock_observer.messages), 1)
        self.assertIn("you have borrowed 'The Great Gatsby'", self.mock_observer.messages[0])

    def test_borrow_book_already_borrowed(self):
        self.borrow_service.borrow_book("M003", "1112223334")
        with self.assertRaises(Exception) as context:
            self.borrow_service.borrow_book("M003", "1112223334")
        self.assertTrue("Book is already borrowed." in str(context.exception))

    def test_return_book_on_time(self):
        self.borrow_service.borrow_book("M003", "1112223334")
        self.borrow_service.return_book("M003", "1112223334", datetime.now())
        self.assertEqual(self.book.status, BookStatus.AVAILABLE)
        self.assertNotIn(self.book, self.member.borrowed_books)
        self.assertEqual(self.member.fines, 0.0)
        self.assertEqual(len(self.mock_observer.messages), 2)
        self.assertIn("successfully returned 'The Great Gatsby'", self.mock_observer.messages[1])

    def test_return_book_late(self):
        self.borrow_service.borrow_book("M003", "1112223334")
        late_date = self.book.due_date + timedelta(days=3)
        self.borrow_service.return_book("M003", "1112223334", late_date)
        self.assertEqual(self.book.status, BookStatus.AVAILABLE)
        self.assertNotIn(self.book, self.member.borrowed_books)
        self.assertEqual(self.member.fines, 6.0)  # 3 days * $2.0
        self.assertEqual(len(self.mock_observer.messages), 3)
        self.assertIn("overdue by 3 days", self.mock_observer.messages[1])
        self.assertIn("successfully returned 'The Great Gatsby'", self.mock_observer.messages[2])

if __name__ == '__main__':
    unittest.main()
