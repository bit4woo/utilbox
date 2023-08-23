# coding: utf-8
from setuptools import setup, find_packages

setup(
    name="utilbox",
    version="0.1.0",
    author="bit4woo",
    author_email="your.email@example.com",
    description="common used functions for me",
    long_description="common used functions for me",
    long_description_content_type="text/markdown",
    url="https://github.com/bit4woo/utilbox",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    python_requires=">=3.8",
)