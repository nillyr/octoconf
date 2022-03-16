from pathlib import Path

from setuptools import setup, find_packages

# from octoconf.__init__ import __version__

current_dir = Path(__file__).resolve().parent

# Quick and dirty fix because tox doesn't like from octoconf.[...]
with open(str(current_dir / "octoconf/__init__.py"), "r") as f:
    version = f.readlines()[0].replace("__version__ = ", "").replace('"', "").rstrip()

with open(str(current_dir / "requirements.txt"), "r") as f:
    requirements = f.readlines()

setup(
    name="octoconf",
    # version=__version__,
    version=version,
    description="Tool for semi-automatic verification of security configurations.",
    url="https://github.com/nillyr/octoconf",
    author="Nicolas GRELLETY",
    author_email="ngy.cs@protonmail.com",
    license="GPLv3+",
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
