#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Joshua Lorincz",
    author_email='joshlor@berkeley.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="An environment that models the behaviour of one or many microgrids",
    entry_points={
        'console_scripts': [
            'mgl2=mgl2.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mgl2',
    name='mgl2',
    packages=find_packages(include=['mgl2', 'mgl2.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lajz/mgl2',
    version='0.1.0',
    zip_safe=False,
)
