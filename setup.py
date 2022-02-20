import os

from setuptools import setup, find_packages

# from octoconf.__init__ import __version__


current_dir = os.path.abspath(os.path.dirname(__file__))

# Quick and dirty fix because tox doesn't like from octoconf.[...]
with open(os.path.join(current_dir, "octoconf/__init__.py"), "r") as f:
    version = f.readlines()[0].replace("__version__ = ", "").replace('"', "").rstrip()

with open(os.path.join(current_dir, "requirements.txt"), "r") as f:
    requirements = f.readlines()

setup(
    name="octoconf",
    # version=__version__,
    version=version,
    description="Tool for semi-automatic verification of security configurations.",
    url="https://github.com/nillyr/octoconf",
    author="Nicolas GRELLETY",
    author_email="ngy.cs@protonmail.com",
    license="MIT",
    python_requires=">=3.8",
    install_requires=requirements,
    packages=find_packages(),
    package_data={
        "": ["*.po"] + ["*/*.yaml"] + ["*/*/*.yaml"] + ["*/*/*/*.yaml"],
    },
    entry_points={
        "console_scripts": [
            "octoconf=console.cli:cli",
        ],
    },
)
