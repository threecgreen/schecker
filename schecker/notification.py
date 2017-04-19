"""
Contains SMSNotifier class for creating objects that send SMS notifications using Twilio.
"""
from twilio.rest import TwilioRestClient

import schecker.config as config


class SMSNotifier(object):
    """
    Object for sending SMS notification messages.
    
    Args:
        default_msg_str: Not implemented features allowing a parametrized message string to be saved within the object.
        
    Attributes:
        _client: Twilio client for sending SMS messages. Authenticated and configured in config.py
        from_phone_number: The phone number sending the SMS messages. Configured in config.py
        default_msg_str: Not implemented features allowing a parametrized message string to be saved within the object.
    """
    def __init__(self, default_msg_str: str=None):
        self._client = TwilioRestClient(config.twilio["account_sid"], config.twilio["auth_token"])
        self.from_phone_number = config.twilio["from_phone_number"]
        # TODO Implement default message string.
        if default_msg_str is not None:
            raise NotImplemented("Default message functionality is not yet implemented. Please provide a full string"
                                 " each time the notify() method is called.")
        self.default_msg_str = default_msg_str

    def __repr__(self):
        return "<SMSNotifier(from_phone_number={0.from_phone_number!r}," \
               " default_msg_str={0.default_msg_str!r})>".format(self)

    def notify(self, message: str, to_phone_number: str):
        """
        Send the passed message as an SMS to the to_phone_number.
        
        Args:
            message: The message to be sent.
            to_phone_number: The receiving phone number of the SMS messages.
        """
        self._client.messages.create(to=to_phone_number,
                                     from_=self.from_phone_number,
                                     body=message)
