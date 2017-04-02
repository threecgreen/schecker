"""
Add SMSNotifier class and check_course_availability function to the main namespace since they are the two objects 
necessary for accomplishing schecker's purpose.
"""
from schecker.course_check import check_course_availability
from schecker.notification import SMSNotifier


__all__ = ["SMSNotifier", "check_course_availability"]
