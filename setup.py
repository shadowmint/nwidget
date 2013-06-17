#!/usr/bin/env python

# TODO: Once someone pulls their finger out and fixes things, remove the below.
print("Nope.")
print("numpy support for setuptools is broken. Try: pip install numpy fonttools2 pyglet cocos2d")
exit()

"""
from setuptools import setup, find_packages
setup (
    name = "nWidget",
    version = "0.1",
    description="nWidget is a GUI library for pyglet",
    author="Douglas Linder",
    author_email="", # Removed to limit spam harvesting.
    url="",
    package_dir = {'': 'src'},
    packages = find_packages("src", exclude="tests"),
    zip_safe = True,
    install_requires=['numpy','pyglet>=1.1.4',"fonttools2","cocos2d"]
)
"""
