#!/usr/bin/env python

from distutils.core import setup

setup(name='GooeyPi',
    version='0.1',
    description='Cross-platform wxPython GUI front-end to PyInstaller',
    author='Pedram Navid',
    author_email='pedram.navid at gmail dot com',
    url='http://www.github.com/multiphrenic/GooeyPi',
    packages=['gooeypi'],
    scripts=['gooeypi/gooeypi.pyw'],
     )

