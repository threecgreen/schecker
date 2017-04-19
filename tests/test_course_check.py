import pytest
from bs4 import BeautifulSoup

from schecker.course_check import find_section, find_registration, parse_registration


@pytest.fixture
def page_bs():
    with open("test_usc_courses_webpage.html", "r") as f:
        html = f.read()
    return BeautifulSoup(html, "html.parser")


@pytest.mark.parametrize("section", ["32872", "32872R", "32876", "49377"])
def test_find_section_find_registration(page_bs, section):
    section_soup = find_section(page_bs, section)
    # Assert is not None
    assert section_soup
    registration_tag = find_registration(section_soup)
    assert "google" not in registration_tag
    assert "of" in registration_tag


def test_parse_registration():
    seats = parse_registration("1 of 2")
    assert seats == 1
