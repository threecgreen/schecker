"""
Contains the main function for running the schecker program to monitor available spots in University of Southern 
California courses and then send SMS notifications when spots become available.

Examples:
    Check availability of the 32872 Lecture section of ENGL 172: The Art of Poetry for the Fall 2017 term and send
    a message to +1 (123) 456-7890 if there are seats available.
    $ python main.py --notify-phone-number +11234567890 --urls https://classes.usc.edu/term-20173/classes/arlt/
      --sections 32872
    
    Multiple sections can be monitored, by listing multiple URLs and section numbers. A URL must be provided for each
    section number to be monitored, even if there are repeat URLs.
    $ python main.py -u https://classes.usc.edu/term-20173/classes/arlt/ https://classes.usc.edu/term-20173/classes/gct 
      -s 32876 10320 -n +11234567890
    
    To check continuously, simply add the --continuous True flag
"""
import argparse
import logging
from time import sleep
from typing import List

from schecker import SMSNotifier, check_course_availability


def main(notify_number: str, urls: List[str], sections: List[str]):
    """
    Checks the given sections for available seats and sends an SMS if there are available spots.
    
    Args:
        notify_number: Number to send the SMS notification to.
        urls: URL(s) from the classes.usc.edu website containing the section information of the courses to be monitored.
        sections: Section number(s) of the class(es) to be monitored.
    """
    sms_notifier = SMSNotifier(notify_number)
    std_message = "{section} now has {num_seats} seats available."

    if len(urls) != len(sections):
        raise ValueError("Must provide the same number of course sections as course URLs, even if there are "
                         "repeat URLs.")
    for url, section in zip(urls, sections):
        seats_available = check_course_availability(url, section)
        if seats_available > 0:
            message = std_message.format(section=section, num_seats=seats_available)
            logging.info("{} available seats found for {}.".format(seats_available, section))
            sms_notifier.notify(message)
            logging.debug("Message sent to {}.".format(notify_number))
        else:
            logging.info("No available seats found for {}.".format(section))


if __name__ == "__main__":
    # Logging configuration
    logging.basicConfig(level=logging.INFO,
                        filename="schecker.log",
                        filemode="a",
                        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                        datefmt="%y-%m-%d %H:%M")

    # Command line argument parser configuration
    parser = argparse.ArgumentParser(
        description="Monitors USC courses for when new openings become available and then sends an SMS notification.",
    )
    parser.add_argument("-n", "--notify-phone-number", type=str, required=True,
                        help="The phone number to send class availability notifications to.")
    # nargs="+" creates a list of str
    parser.add_argument("-u", "--urls", action="store", type=str, nargs="+", required=True,
                        help="The USC classes URL containing the course.")
    parser.add_argument("-s", "--sections", action="store", type=str, nargs="+", required=True,
                        help="The section code for the desired course.")
    parser.add_argument("-c", "--continuous", type=bool, required=False,
                        help="Whether to run the program continuously (i.e. in an infinite loop).")
    args = parser.parse_args()
    if args.continuous:
        logging.info("Starting continuous running.")
        while True:
            main(args.notify_phone_number, args.urls, args.sections)
            # Run every two minutes
            sleep(240)
    else:
        # Run once
        main(args.notify_phone_number, args.urls, args.sections)
