#!/usr/bin/env python

from setuptools import setup

setup(
    name='timezones',
    version='2.0.3',
    author="Doist Developers",
    author_email="dev@doist.com",
    url="https://doist.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=['timezones'],
    install_requires=[
        'geoip2',
        'pytz',
        'future',
    ],
    platforms=["Any"],
    license="MIT",
    keywords='timezones timezone pytz',
    description=
    "A Python library that provides better selection of common timezones, can output HTML and auto select the best timezone based on user's IP.",
    long_description="""\
python-timezones
----------------

A Python library that provides better selection of common timezones,
can output HTML and auto select the best timezone based on user's IP.

Visit http://doist.github.com/python-timezones/ for more information.

Copyright: 2012-2019 by Doist
License: MIT.""")
