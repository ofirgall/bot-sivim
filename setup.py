#!/usr/bin/env python3

import setuptools
from pathlib import Path

setuptools.setup(
    name='bot_sivim',
    version='1.0.0',
    description='Telegram bot to check fiber availability',
    long_description_content_type='text/markdown',
    url='https://github.com/ofirgall/bot-sivim',
    author='Ofir Gal',
    author_email='',
    packages=setuptools.find_packages(),
    install_requires=['python-telegram-bot>=13.11'],
    classifiers=[
    ],
    python_requires='>=3.8',
)
