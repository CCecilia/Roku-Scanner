import pathlib

from setuptools import setup

# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
README = (cwd / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="roku-scanner",
    version="1.0.0",
    description="Scans LAN for and Roku devices and gives device information",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/CCecilia/Roku-Scanner",
    author="Christian Cecilia",
    author_email="christian.cecilia1@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["roku_scanner"],
    include_package_data=True,
    install_requires=[
        "requests",
        "xmltodict"
    ],
    entry_points={
        "console_scripts": [
            "roku_scanner=roku_scanner.__main__:main",
        ]
    },
)