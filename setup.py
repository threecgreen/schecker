"""
Setuptools module for package installation.
"""
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession
from os import path


here = path.abspath(path.dirname(__file__))

# parse_requirements() returns a generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=PipSession())

# Create list of required packages
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="schecker",
    version="0.2.0",
    description="Monitors and notifies when requested USC courses open up.",
    author="Carter Green",
    license="MIT License",
    packages=find_packages(exclude=[".cache", ".idea", "doc", "tests"]),
    install_requires=reqs,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
