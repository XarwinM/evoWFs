from setuptools import setup, find_packages

setup(
    name="evoWFs",
    version="1.0",
    description="A module to learn WFs with evolutionary algorithms",
    author="Jens Mueller",
    author_email="jens.mueller1492@gmail.com",
    # packages=['evoWFs'],  #same as name
    packages=find_packages(),
    install_requires=[],  # external packages as dependencies
)
