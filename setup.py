#!/usr/bin/env python

from distutils.core import setup

project_name = "pylings"
version = "0.1.0"
description = ""
author = "Alessio Izzo"
author_email = "alessio.izzo86@gmail.com"
readme = "README.md"
requirements = [
    'watchdog==2.2.1',
    'pytest==7.2.1',
    'pyyaml==6.0',
    'pyfiglet==.7',
    'tqdm==4.64.1',
]

setup(
    name=project_name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    readme=readme,
    url='https://github.com/aless10/pylings/',
    packages=['src', 'exercises', 'tests'],
    install_requires=requirements,
    entry_points={
        'console_scripts': ['pylings=src.main:main']
    },
    classifiers=[
          'Development Status :: 1 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: Software Development :: Bug Tracking',
          ],
)
