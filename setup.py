import os

from setuptools import setup, find_packages

from octoreconf.__init__ import __version__

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "requirements.txt"), "r") as f:
    requirements = f.readlines()

setup(
    name="octoreconf",
    version=__version__,
    description="Tool for semi-automatic verification of security configurations.",
    url="https://github.com/Nillyr/octoreconf",
    author="Nicolas GRELLETY",
    author_email="ngy.cs@protonmail.com",
    license="MIT",
    python_requires=">=3.7",
    install_requires=requirements,
    packages=find_packages(),
    package_data={
        "": ["*.po"] + ["*/*.yaml"],
    },
    entry_points={
        "console_scripts": [
            "octoreconf=console.cli:cli",
        ],
    },
)
