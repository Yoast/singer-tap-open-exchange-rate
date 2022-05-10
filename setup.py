"""Setup."""
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='tap-open-exchange',
    version='0.1.0',
    description='Singer.io tap for extracting historical data from Open Exchange Rate',
    author='Yoast',
    url='https://github.com/Yoast/singer-tap-open-exchange-rate',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['tap_open_exchange'],
    install_requires=[
        'httpx[http2]~=0.16.1',
        'python-dateutil~=2.8.1',
        'singer-python~=5.10.0',
    ],
    entry_points="""
        [console_scripts]
        tap-open-exchange=tap_open_exchange:main
    """,
    packages=find_packages(),
    package_data={
        'tap_open_exchange': [
            'schemas/*.json',
        ],
    },
    include_package_data=True,
)
