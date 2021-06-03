# setup.py  
# This file is part of jupylecture
# Author Roelof Rietbroek (r.rietbroek@utwente.nl), 2021
import setuptools
from setuptools import find_packages
import os


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="jupylecture",
    author="Roelof Rietbroek",
    author_email="roelof@wobbly.earth",
    version="1.0",
    description="Python tools to facilitate working with jupyter rise presentations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/strawpants/jupylecture",
    packages=find_packages("."),
    include_package_data=True,
    scripts=['jupylecture2pdf.sh','jupylectureinit.py'],
    install_requires=['lxml'],
    classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education",
        "Intended Audience :: Education",
        "Development Status :: 4 - Beta"]
)
