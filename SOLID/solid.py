from abc import ABC, abstractmethod

# --- S: Single Responsibility ---
# Each class has one job.
# Message only holds data, EmailNotifier/SMSNotifier only send.
class Message:
    def __init__(self, content: str):
        self.content = content

# --- O: Open/Closed ---
# Add SlackNotifier without touching existing classes.
class Notifier(ABC):
    @abstractmethod
    def send(self, message: Message) -> None:
        pass

class EmailNotifier(Notifier):
    def send(self, message: Message) -> None:
        print(f"Email sent: {message.content}")

class SMSNotifier(Notifier):
    def send(self, message: Message) -> None:
        print(f"SMS sent: {message.content}")

""" Example of new notifier

class SlackNotifier(Notifier):

"""

# --- L: Liskov Substitution ---
# Any subclass of Notifier can replace another.
# notify_user works with any Notifier.
def notify_user(notifier: Notifier, message: Message) -> None:
    notifier.send(message)

# --- I: Interface Segregation ---
# Notifier interface is minimal.

# --- D: Dependency Inversion ---
# notify_user depends on Notifier abstraction, not specific implementations.

if __name__ == "__main__":
    msg = Message("Meeting at 10 AM")
    email = EmailNotifier()
    sms = SMSNotifier()

    notify_user(email, msg)
    notify_user(sms, msg)
