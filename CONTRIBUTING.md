# Welcome to this contibuting guide

## Getting started

### Clone the source code

From the LAN, run the following command:

```bash
git clone --recurse-submodules -j8 ssh://git@gitlab.internal.lan:2222/octo-project/octoconf.git
```

If cloning from GitHub:

```bash
# Clone without initializing submodules
git clone git@github.com:nillyr/octoconf.git
cd octoconf

# Update submodules URL
## from: ssh://git@gitlab.internal.lan:2222/octo-project/<repo>.git
## to: ssh://git@github.com:nillyr/<repo>.git
bash scripts/update_gitmodules_url_for_github.sh

# Init and update submodules
git submodule update --init --recursive
```

### Installation

Create a virtual environment and install all (base+dev) requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ."[dev]"
```

### Develop

This project use the `clean architecture`. Here are some links:

- [Clean architectures in Python: a step-by-step example](https://www.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/)
- [Python & the Clean Architecture in 2021](https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/)
- [The Clean Architecture in Python. How to write testable and flexible code](https://breadcrumbscollector.tech/the-clean-architecture-in-python-how-to-write-testable-and-flexible-code/)

### Test

```bash
# With Makefile
make test
# With pytest
pytest -v
```

### Build

```bash
# prerequisites: python3-build
make build
```

### Upload to PyPI

```bash
twine upload dist/*
```
