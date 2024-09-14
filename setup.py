#!/usr/bin/env python

from distutils.core import setup

setup(
    name='matrix-notify',
    version='1.0.0',
    description='Send matrix messages to a room.',
    long_description='Import this Python package to send messages to a matrix room, optionally with end-to-end encryption.',
    author='Fabian Fuchs',
    license='GPL-3.0-or-later',
    url='https://github.com/fuchs-fabian/matrix-notify-py',
    keywords=['matrix', 'element', 'notify'],
    platforms=['Linux'],
    python_requires='>=3.10',
    install_requires=[
        'requests',
        'matrix-commander',
    ],
    entry_points={
        'console_scripts': [
            'matrix-notify=matrix_notify:_process_arguments_and_send_message',
        ],
    },
)