from distutils.core import setup

long_description = open('README.rst').read()

setup(
    name='django-gatekeeper',
    version="0.1",
    package_dir={'gatekeeper': 'gatekeeper'},
    packages=['gatekeeper'],
    package_data={'gatekeeper': ['templates/admin/gatekeeper/*.html']},
    description='Django object moderation',
    author='Jeremy Carbaugh',
    author_email='jcarbaugh@sunlightfoundation.com',
    license='BSD License',
    url='http://github.com/sunlightlabs/django-gatekeeper/',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)