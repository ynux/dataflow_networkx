"""
From:
https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages

setup(
    name='table_view_dependencies', 
    version='0.0.1',
    description='analyzing view / table dependencies in networkx',
    author_email='suny.kim@btelligent.com', 
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5',
    install_requires=['networkx==2.2', 'nxviz'],
)
