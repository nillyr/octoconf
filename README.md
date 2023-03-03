# octoconf

<p align="center">
  <img width="200" height="200" src="resources/logo.png">
  <br/><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img src="https://img.shields.io/badge/platform-Linux%2FmacOS%2FWindows-blue.svg">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg">
  </br>
  <img src="https://github.com/nillyr/octoconf/actions/workflows/snyk.yml/badge.svg">
  <img src="https://github.com/nillyr/octoconf/actions/workflows/tests.yml/badge.svg">
  <img src="https://img.shields.io/badge/coverage-96%25-green.svg">
</p>

Tool dedicated to the realization of configuration audits of various assets.

```
        ,'""`.       octoconf 2.0.0b
       / _  _ \
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\
     (( ((  )) ))    /** @nillyr **/
   hh `\ `)(' /'


positional arguments:
  {analyze,audit,baseline,report} Available Commands
    analyze             performs an analysis on an archive based on a security baseline
    baseline            performs the interaction with the security baselines
    report              performs the recompilation of the report in PDF format from an adoc file
    config              performs octoconf configuration management

optional arguments:
  -h, --help            show this help message and exit
  --version             print version and exit
  -d, --debug           debug output (verbose)
```

## Prerequisites

- Python 3.8+
- pip
- Asciidoc:
  - [Asciidoctor](https://docs.asciidoctor.org/asciidoctor/latest/install/) processor: `asciidoctor-pdf`
  - [ruby-rouge](https://docs.asciidoctor.org/asciidoctor/latest/syntax-highlighting/rouge/)

## Documentation

- Documentation can be found in the [wiki](https://github.com/nillyr/octoconf/wiki).

## Quick usage

- Clone this repo:

```bash
git clone --recurse-submodules git@github.com:nillyr/octoconf.git
```

- Generation of the script from a baseline:

```bash
# Generate a collection script
python console/cli.py baseline generate_script -p linux -b ./debian-based.yml -o audit-debian.sh
# Generate a collection script with utils functions included
python console/cli.py baseline generate_script -p linux -b ./debian-based.yml -u ./utils.sh -o audit-debian.sh
```

- Analyze of the results:

```bash
# Retrieve audit evidence and then analyze
python console/cli.py analyze -b ./debian-based.yml -a [...].zip
```

When using [octowriter](https://github.com/nillyr/octowriter) submodule, a `.ini` file can be use to init the PDF report.

Create the following file with your own values:

```ini
[DEFAULT]
auditee_name = Tricatel
auditee_contact_full_name = Jacques Tricatel
auditee_contact_email = Jacques.Tricatel@tricatel.fr

project_manager_full_name = Charles Duchemin
project_manager_email = Charles.Duchemin@guide-duchemin.fr

authors_list_full_name = Charles Duchemin; Gérard Duchemin
authors_list_email = Charles.Duchemin@guide-duchemin.fr; Gérard.Duchemin@guide-duchemin.fr

audited_asset = canning-worker1.tricatel.lan

confidentiality_level = Confidential
```

Analyze of the results:

```bash
python console/cli.py analyze -b ./debian-based.yml -a [...].zip --ini info.ini
```

In order to use a custom theme with your own images, the following command can be used:

```bash
python console/cli.py analyze -b ./debian-based.yml -a [...].zip --ini info.ini --imagesdir /path/to/imagesdir --pdf-themesdir /path/to/themesdir --pdf-theme custom-theme.yml
```

## Disclaimer

- This is not a turn key tool, read the documentation for more information
- This tool does not offer any guarantee
- The authors of this tool cannot be held responsible for the effects caused by the executed commands
- It is highly recommended to risk assess your commands in a test environment before using them in production

## Maintainer

- [Nicolas GRELLETY](https://github.com/nillyr)

## Authors

- [Nicolas GRELLETY](https://github.com/nillyr)

## Copyright and license

Copyright (c) 2021-2023 [Nicolas GRELLETY](https://github.com/nillyr)

This software is licensed under GNU GPLv3 license. See `LICENSE` file in the root folder of the project.

The information used in the configuration file comes from the movie "[L'Aile ou la Cuisse](https://www.allocine.fr/film/fichefilm_gen_cfilm=47573.html)".

Icons made by [Smashicons](https://www.flaticon.com/authors/smashicons "Smashicons") from [www.flaticon.com](https://www.flaticon.com/ "Flaticon")
