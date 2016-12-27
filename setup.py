#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from setuptools import setup

setup(name='timezones',
      version = '1.9.7',
      author="amix",
      author_email="amix@amix.dk",
      url="http://www.amix.dk/",
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
        'pytz'
      ],
      platforms=["Any"],
      license="MIT",
      keywords='timezones timezone pytz',
      description="A Python library that provides better selection of common timezones, can output HTML and auto select the best timezone based on user's IP.",
      long_description="""\
timezones
---------------

A Python library that provides better selection of common timezones, can output HTML and auto select the best timezone based on user's IP.

Visit http://doist.github.com/python-timezones/ for more information.

Copyright: 2012 by Doist
License: MIT.""")
