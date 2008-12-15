#!/usr/bin/env python

from distutils.core import setup

setup(
    name='gatekeeper',
    version='0.1',
    description='Simple object moderation',
    long_description='Moderate any object in a Django application.',
    license='BSD License',
    author='Jeremy Carbaugh',
    author_email='jcarbaugh@sunlightfoundation.com',
    url='http://code.google.com/p/django-gatekeeper/',
    download_url='http://code.google.com/p/django-gatekeeper/downloads/list',
    packages=['gatekeeper'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
)