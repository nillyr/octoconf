# octoconf

<p align="center">
  <img width="200" height="200" src="resources/logo.png">
  <br/><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img src="https://img.shields.io/badge/platform-Linux%2FmacOS%2FWindows-blue.svg">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg">
  <img src="https://img.shields.io/badge/Changelog-gitmoji-brightgreen.svg">
  <a href="https://twitter.com/n1llyr">
    <img alt="Twitter: n1llyr" src="https://img.shields.io/twitter/follow/n1llyr.svg?style=social" target="_blank" />
  </a>
</p>

Tool dedicated to the realization of configuration audits of various assets.

| :information_source: Information |
|:-------------------------------------------------------------|
| This repository is mirrored from a private GitLab instance |

```
        ,'""`.       octoconf 2.0.0-beta
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
  - [Asciidoctor](https://docs.asciidoctor.org/asciidoctor/latest/install/) processor: [asciidoctor-pdf](https://docs.asciidoctor.org/pdf-converter/latest/install/)
  - [ruby-rouge](https://docs.asciidoctor.org/asciidoctor/latest/syntax-highlighting/rouge/)

## Documentation

- TODO

## Quick usage

- Clone this repo:

```bash
# Cloning from GitHub

## Clone without initializing submodules
git clone git@github.com:nillyr/octoconf.git
cd octoconf

## Update submodules URL
bash update_gitmodules_url_for_github.sh

## Init and update submodules
git submodule update --init --recursive
```

- Create a virtual environment and install requirements

```bash
bash setup.sh
```

- Active the virtual environment

```bash
source venv/bin/activate
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

When using [octowriter](https://gitlab.internal.lan/octo-project/octowriter) ([GitHub link](https://github.com/nillyr/octowriter)) submodule, a `.ini` file can be use to init the PDF report.

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

classification_level = Confidential

auditor_company_name = Guide Duchemin
```

Analyze of the results:

```bash
python console/cli.py analyze -b ./debian-based.yml -a [...].zip -o "`pwd`/reports/" --ini info.ini
```

In order to use a custom theme with your own images, the following command can be used:

```bash
python console/cli.py analyze -b ./debian-based.yml -a [...].zip -o "`pwd`/reports/" --ini info.ini --template-name <my_template_name> --pdf-theme <my_theme.yml>
```

In order to re-generate the PDF report, the following command can be used:

```bash
python console/cli.py report -i "`pwd`/reports/build/adoc/header.adoc" -o "`pwd`/reports/" --template-name <my_template_name> --pdf-theme <my_theme.yml>
```

## Troubleshooting

### Microsoft Excel

If you got the following errors when opening the `.xlsx` file, you first need to use this [conversion script](https://gitlab.internal.lan/octo-project/octokonverter/-/blob/main/scripts/octoconf_xlsx_to_ms_excel.py) ([GitHub link](https://github.com/nillyr/octokonverter/blob/main/scripts/octoconf_xlsx_to_ms_excel.py))

![excel-err1](resources/non-excel-open-on-ms-excel.png)
![excel-err2](resources/non-excel-open-on-ms-excel-2.png)

## Disclaimer

- This is not a turn key tool, read the documentation for more information
- This tool does not offer any guarantee
- The authors of this tool cannot be held responsible for the effects caused by the executed commands
- It is highly recommended to risk assess your commands in a test environment before using them in production

## Maintainer

- Nicolas GRELLETY

## Authors

- Nicolas GRELLETY

## Copyright and license

Copyright (c) 2021 Nicolas GRELLETY

This software is licensed under GNU GPLv3 license. See `LICENSE` file in the root folder of the project.

The information used in the configuration file comes from the movie "[L'Aile ou la Cuisse](https://www.allocine.fr/film/fichefilm_gen_cfilm=47573.html)".

Icons made by [Freepik](https://www.flaticon.com/authors/freepik "Freepik") from [www.flaticon.com](https://www.flaticon.com/ "Flaticon")
