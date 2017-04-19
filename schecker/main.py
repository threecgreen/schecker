"""
Contains the main function for running the schecker program to monitor available spots in University of Southern 
California courses and then send SMS notifications when spots become available.

To check continuously, simply add the --continuous True flag
"""
import argparse
import logging
from time import sleep
from typing import List

import schecker.config as config
from schecker import check_course_availability, CourseToCheck, SMSNotifier


def check_and_notify(sms_notifier: SMSNotifier, courses_to_check: List[CourseToCheck]) -> List[CourseToCheck]:
    """
    Checks the given sections for available seats and sends an SMS if there are available spots.
    
    Args:
        sms_notifier:
        courses_to_check: 
    
    Returns: Remaining courses_to_check (those for which open seats haven't been found).
    """
    std_message = "{course}\nSection {section} now has {num_seats} seats available."

    for i, course in enumerate(courses_to_check):
        try:
            seats_available = check_course_availability(course.schedule_url, course.course_section_number)
        except ConnectionResetError:
            logging.warning("ConnectionResetError was caught; waiting two minutes to try again.")
            sleep(120)

        if seats_available > 0:
            message = std_message.format(course=course.name, section=course.section_number, num_seats=seats_available)
            logging.info("{num_seats} available seats found for {course} section {section}."
                         .format(num_seats=seats_available, course=course.name, section=course.section_number))
            sms_notifier.notify(message, course.contact_phone_number)
            logging.debug("Message sent to {}.".format(course.contact_phone_number))
            courses_to_check.pop(i)
            logging.debug("{} removed from list of courses to check".format(course.name))
        else:
            logging.info("No available seats found for {course} section {section}."
                         .format(course=course.name, section=course.section_number))
    return courses_to_check


def main(continuous: bool):
    sms_notifier = SMSNotifier()
    courses_to_check = config.courses_to_check
    if continuous:
        logging.info("Starting continuous running.")
        while courses_to_check:
            courses_to_check = check_and_notify(sms_notifier, courses_to_check)
            # Run every eight minutes
            sleep(480)
        logging.info("Available seats found for all courses in config.py")
    else:
        # Run once
        check_and_notify(sms_notifier, courses_to_check)


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
    parser.add_argument("-c", "--continuous", type=bool, required=False,
                        help="Whether to run the program continuously (i.e. in an infinite loop).")
    args = parser.parse_args()
    main(args.continuous)
