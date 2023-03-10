from setuptools import setup, find_packages

from strite_data_hub import __version__

setup(
    name="strite_data_hub",
    version=__version__,
    url="https://github.com/strite-ru/strite-data-hub",
    author="Alex Ruban",
    author_email="ruban_1998@hotmail.com",
    description="",
    py_modules=["strite_data_hub"],

    packages=find_packages(exclude=['tests', 'tests.*']),
)
