# coding: utf-8
from setuptools import setup

setup(
    name="utilbox",
    version="0.1.0",
    author="bit4woo",
    author_email="your.email@example.com",
    description="common used functions for me",
    long_description="common used functions for me",
    long_description_content_type="text/markdown",
    url="https://github.com/bit4woo/utilbox",
    packages=["utilbox"],
    install_requires=[
        "requests",
        "beautifulsoup4",
        "PySocks",
    ],
    python_requires=">=3.8",
)