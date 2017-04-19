"""
This is a template for config.py, a module containing program configuration information:
    Twilio API keys in order to send text messages. 
    A list containing the classes, sections and URL to check with the accompanying contact phone numbers.
    
This actual module should be ignored by git.
"""
from schecker import CourseToCheck


# Twilio API keys and from phone number (provided by Twilio)
twilio = {
    "from_phone_number": "",
    "account_sid": "",
    "auth_token": "",
}

# List with each key being the class name (or whatever the name the user wants to use for the course)
courses_to_check = [
    CourseToCheck(name="Name of the class", section_number="101", schedule_url="URL from classes.usc.edu",
                  contact_phone_number="+11234567890"),
]

