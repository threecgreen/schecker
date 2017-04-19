"""
Contains the CourseToCheck namedtuple used for program configuration and all logic for checking class availability 
from the classes.usc.edu website.
"""
import logging
import re
import requests
from bs4 import BeautifulSoup
from collections import namedtuple


CourseToCheck = namedtuple("CourseToCheck", ["name", "section_number", "schedule_url",
                                             "contact_phone_number"])


def get_webpage_soup(url: str) -> BeautifulSoup:
    """
    Get the BeautifulSoup object for the given website.
    
    Args:
        url: URL of the website.

    Returns: BeautifulSoup object of the website's HTML.
    """
    page = requests.get(url)
    return BeautifulSoup(page.text, "html.parser")


def find_section(soup: BeautifulSoup, section: str) -> BeautifulSoup:
    """
    Find HTML of the given course section and return a new BeautifulSoup object containing only the section's HTML.
    
    Args:
        soup: Webpage's soup.
        section: Course section code.

    Returns: BeautifulSoup of the section's HTML.
    """
    section = section.upper()
    # Only search for section number; ignore letters (and all non-numerics)
    section = re.sub("[^0-9]+", "", section)
    result = soup.find("tr", {"class": section})
    return BeautifulSoup(str(result), "html.parser")


def find_registration(section_soup: BeautifulSoup) -> str:
    """
    Find the registration tag within the course section's HTML.
    
    Args:
        section_soup: BeautifulSoup of the course section's HTML.

    Returns: The registration tag's relevant content, ignoring Google search tags.
    """
    register_td = section_soup.find("td", {"class": "registered"})
    try:
        return register_td.div.contents[0]
    except AttributeError:
        # Ignore contents 0 and 2 because they are google tags
        return register_td.contents[1]


def parse_registration(registration_contents: str) -> int:
    """
    Parses the registration tag's HTML content to find out how many seats are available.
    
    Args:
        registration_contents: Registration tag's HTML content.

    Returns: The number of available seats in the course section.
    """
    # Remove any Google tags
    # registration_contents = registration_contents.replace("<!--googleoff: index-->", "")
    # registration_contents = registration_contents.replace("<!--googleon: index-->", "")
    logging.debug(registration_contents)
    # Separate number registered and total slots and convert to ints within a tuple
    registered = [int(x) for x in registration_contents.split(" of ")]
    return registered[1] - registered[0]


def check_course_availability(url: str, section: str) -> int:
    """
    Ties all the small functions together to provide a simple way checking course availability.
    
    Args:
        url: URL from the classes.usc.edu website containing the information for the desired course.
        section: Section number to check seat availability.

    Returns: Number of seats available in the section.
    """
    page_soup = get_webpage_soup(url)
    section_soup = find_section(page_soup, section)
    logging.debug("Section soup: {}".format(section_soup))
    if section_soup is None:
        logging.warning("The requested section ({}) could not be located in the given HTML.".format(section))
        return 0
    registration_content = find_registration(section_soup)
    logging.debug("Registration content: {}".format(registration_content))
    if registration_content is None:
        logging.warning("The registration HTML could not be properly parsed for section {}.".format(section))
        return 0
    return parse_registration(registration_content)


