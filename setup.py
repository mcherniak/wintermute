#!/usr/bin/env python
from setuptools import setup

setup(name='wintermute',
      version='1.0',
      description='IPAM',
      author='Mikhail Cherniak',
      author_email='mikcherniak@gmail.com',
      url='',
      install_requires=['netaddr', 'flask', 'flask-bootstrap', 'redis'],
    )