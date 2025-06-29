from setuptools import setup, find_packages

setup(
    name="dna_sonification",
    version="0.1.0",
    packages=find_packages(where="sonification"),
    package_dir={"": "sonification"},
)