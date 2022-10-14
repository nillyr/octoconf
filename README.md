# octoconf

<p align="center">
  <img width="200" height="200" src="ressources/logo.png">
  <br/><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img src="https://img.shields.io/badge/platform-Linux%2FmacOS%2FWindows-blue.svg">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg">
  </br>
  <img src="https://github.com/nillyr/octoconf/actions/workflows/snyk.yml/badge.svg">
  <img src="https://github.com/nillyr/octoconf/actions/workflows/tests.yml/badge.svg">
  <img src="https://img.shields.io/badge/coverage-80%25-green.svg">
</p>

Tool dedicated to the realization of configuration audits of various systems via semi-automated analysis of the collected security configurations.

```
        ,'""`.       octoconf 1.6.3rc1
       / _  _ \
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\
     (( ((  )) ))    /** Nicolas GRELLETY ( ngy.cs@protonmail.com ) **/
   hh `\ `)(' /'


positional arguments:
  {analyze,audit,checklist,report} Available Commands
    analyze             performs an analysis on an archive based on a checklist
    audit               performs an audit of the host based on a checklist
    checklist           performs the interaction with the checklists
    report              performs the generation of audit reports

optional arguments:
  -h, --help            show this help message and exit
  --version             print version and exit
  -d, --debug           debug output (verbose)
```

## Prerequisites

- Python 3.8+
- pip

## Documentation

- Documentation can be found in the [wiki](https://github.com/nillyr/octoconf/wiki).
- Documentation can be generated with `pandoc` with `make doc`. The chosen format is `pdf`.

## Quick usage

```bash
# Generate a collection script
octoconf checklist generate -c ./debian-based.yml -p linux -o audit-debian.sh
# Run the script on the targeted host (admin)
chmod +x audit-debian.sh; ./audit-debian.sh
# Retrieve audit evidence and then analyze
octoconf analyze -c ./debian-based.yml -a audit_[...].zip
```

## Disclaimer

- This is not a turn key tool, read the documentation for more information
- This tool does not offer any guarantee
- The authors of this tool cannot be held responsible for the effects caused by the commands made in the checklists
- It is highly recommended to risk assess your checklists in a test environment before using them in production
- It is highly recommended to manually check each critical configuration of the audited system

## Maintainer

- [Nicolas GRELLETY](https://github.com/nillyr)

## Authors

- [Nicolas GRELLETY](https://github.com/nillyr)

## Copyright and license

Copyright (c) 2021-2022 [Nicolas GRELLETY](https://github.com/nillyr)

This software is licensed under GNU GPLv3 license. See `LICENSE` file in the root folder of the project.

Icons made by [Smashicons](https://www.flaticon.com/authors/smashicons "Smashicons") from [www.flaticon.com](https://www.flaticon.com/ "Flaticon")
