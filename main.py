# main.py
from in_memory_repositories import InMemoryBookRepository, InMemoryMemberRepository
from factories import BookFactory
from services import BorrowService, NotificationScheduler
from notifications import NotificationService, EmailNotification
from utils import EmailService
from datetime import datetime, timedelta
from models import MembershipType, Member

def main():
    # Initialize repositories
    book_repo = InMemoryBookRepository()
    member_repo = InMemoryMemberRepository()

    # Initialize factory
    book_factory = BookFactory()

    # Create books
    book1 = book_factory.create_book("1984", "George Orwell", "1234567890", "Dystopian")
    book2 = book_factory.create_book("To Kill a Mockingbird", "Harper Lee", "0987654321", "Classic")
    book_repo.add_book(book1)
    book_repo.add_book(book2)

    # Create members
    member1 = Member("Alice", "M001", MembershipType.PREMIUM)
    member2 = Member("Bob", "M002", MembershipType.STANDARD)
    member_repo.add_member(member1)
    member_repo.add_member(member2)

    # Setup notifications
    email_service = EmailService()
    email_notification = EmailNotification(email_service)
    notification_service = NotificationService()
    notification_service.attach(email_notification)

    # Initialize services
    borrow_service = BorrowService(book_repo, member_repo, notification_service)
    scheduler = NotificationScheduler(member_repo, book_repo, notification_service)

    # Borrow books
    borrow_service.borrow_book("M001", "1234567890")  # Alice borrows 1984
    borrow_service.borrow_book("M002", "0987654321")  # Bob borrows To Kill a Mockingbird

    # Simulate returning books
    # Alice returns on time
    borrow_service.return_book("M001", "1234567890", datetime.now())

    # Bob returns late
    late_return_date = book2.due_date + timedelta(days=5)
    borrow_service.return_book("M002", "0987654321", late_return_date)

    # Check due dates for notifications
    scheduler.check_due_dates()

if __name__ == "__main__":
    main()
