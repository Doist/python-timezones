#!/usr/bin/env python
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, "README.md"), "rt") as f:
    long_description = "\n" + f.read()


version_mod = {}
with open(os.path.join(here, "timezones", "__version__.py")) as f:
    exec(f.read(), version_mod)


setup(
    name="timezones",
    version=version_mod["__version__"],
    author="Doist Developers",
    author_email="dev@doist.com",
    url="https://doist.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["timezones"],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=["geoip2", "pytz", "future"],
    platforms=["Any"],
    license="MIT",
    keywords="timezones timezone pytz",
    description=(
        "A Python library that provides better selection of common "
        "timezones, can output HTML and auto select the best timezone "
        "based on user's IP."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
