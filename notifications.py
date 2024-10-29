# notifications.py
from abc import ABC, abstractmethod
from typing import List
from models import Book, Member

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self, message: str):
        pass

class NotificationService(Subject):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class EmailNotification(Observer):
    def __init__(self, email_service):
        self.email_service = email_service

    def update(self, message: str):
        self.email_service.send_email(message)
