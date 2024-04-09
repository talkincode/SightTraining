#!/usr/bin/env python3

from setuptools import setup, find_packages

readme = """
SightTraining  is a game for children's amblyopia training
"""

setup(
    name="SightTraining",
    version="0.1.23",
    author="jett.wang",
    author_email="jamiesun.net@gmail.com",
    description="SightTraining  is a game for children's amblyopia training",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pygame==2.5.1",
        "python-dotenv>=1.0.1"
    ],
    python_requires='>=3.10',
    entry_points={
        "console_scripts": [
            "spacex01 = spacedefense:runapp"
        ]
    },
)