# Developer documentation

The following documentation is intended for developers.

## Prerequisites

The following prerequisites are required:

- [pandoc](https://pandoc.org/installing.html#)
  - [TeX Live](https://www.tug.org/texlive/) (Linux)
  - [BasicTeX](https://www.tug.org/mactex/morepackages.html) (macOS)
  - [MiKTeX](https://miktex.org) (Windows)
- [upx](https://upx.github.io)

## Developer installation

```bash
# Clone the repo with submodules
git clone --recurse-submodules https://github.com/Nillyr/octoreconf.git
cd octoreconf
# Install on Linux/Unix
bash ./setup.sh
# Install on Windows
.\setup.bat
```

_Note:_ when installed from source, the tool can be run with the following command:

```bash
python console/cli.py
```

## Contributing

Thank you for contributing to make this tool even better.

### Rules

Please respect the following rules:

- It is forbidden to push directly on the main branch
- Any push request / merge request must be linked to an issue
- All additional code must have the most exhaustive unit tests possible
- All new functionality must be documented
- [PEP8](https://www.python.org/dev/peps/pep-0008/) must be followed
- [PEP257](https://www.python.org/dev/peps/pep-0257/) must be followed
- The "Clean architecture" must be respected

## How-to: Build

```bash
make
```
