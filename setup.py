# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='eart',
    version='0.0.1',
    description='provide a generic algorithm',
    author='Yukihiro Ide',
    packages=find_packages(),
    install_requires=['numpy', 'joblib'],
)

