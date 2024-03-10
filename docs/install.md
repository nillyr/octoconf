# Installation of octoconf

## Table of contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Regular usage](#regular-usage)
    - [Advanced users and contributors](#advanced-users-and-contributors)

## Prerequisites

- Python 3.8+
- pip
- Asciidoc:
  - [Asciidoctor](https://docs.asciidoctor.org/asciidoctor/latest/install/)
  - [asciidoctor-pdf](https://docs.asciidoctor.org/pdf-converter/latest/install/)
  - [ruby-rouge](https://docs.asciidoctor.org/asciidoctor/latest/syntax-highlighting/rouge/)

## Installation

### Regular usage

| :warning: Warning |
|:------------------|
| The tool has not been uploaded to PyPI (yet), use the [CONTRIBUTING](../CONTRIBUTING.md) documentation for now. |

Install the latest version from [PyPI](https://pypi.org/project/octoconf-cli/) (recommended) or from the release page.

```bash
# From PyPI
pip install -U octoconf-cli
# From release page
pip install octoconf-*.whl
```

### Advanced users and contributors

This method is recommended, for example, if you want to create your own templates and need to change the submodule URL with your fork. See [CONTRIBUTING](,,/CONTRIBUTING.md) for more information.

