#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

setup(
    name="twitter_easy_streamer",
    description="Easily stream tweets",
    author="Wieden+Kennedy",
    author_email="nilesh.ashra@wk.com",
    url="https://github.com/wieden-kennedy/twitter-easy-streamer",
    version="0.0.1",
    install_requires=["tweepy", "argparse"],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)