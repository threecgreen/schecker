import pytest

from schecker.main import check_and_notify
from schecker import CourseToCheck


@pytest.fixture
def sms_notifier():
    class SMSNotifier(object):
        def __init__(self):
            pass

        @staticmethod
        def notify(self, message, phone_number):
            return message, phone_number
    return SMSNotifier()


@pytest.fixture
def courses_to_check():
    pass


def test_check_and_notify():
    pass
