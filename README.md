# octoreconf

<p align="center">
  <img width="200" height="200" src="ressources/logo.png">
  <br/><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/coverage-80%25-green.svg">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg">
  <img src="https://img.shields.io/badge/platform-macOS%2FLinux%2FWindows-blue.svg">
</p>

Tool dedicated to the realization of configuration audits of various systems via semi-automated analysis of the collected security configurations.

```
        ,'""`.       octoreconf 1.4.0rc1
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

- Python 3.7+
- pip

## Documentation

The documentation is available in `pdf` format. See the [releases](https://github.com/Nillyr/octoreconf/releases) page.

## Quick usage

```bash
# Generate a collection script
octoreconf checklist generate -c desktop/windows10 -l powershell -p windows -o windows10.ps1
# Run the script on the targeted host (admin)
powershell.exe -nop -exec bypass .\windows10.ps1
# Retrieve audit evidence and then analyze
octoreconf analyze -c desktop/windows10 -a Audit[...].zip
```

## Disclaimer

- This is not a turn key tool, read the documentation
- This tool does not offer any guarantee
- The authors of this tool cannot be held responsible for the effects caused by the commands made in the checklists
- It is highly recommended to risk assess your checklists in a test environment before using them in production
- It is highly recommended to manually check each critical configuration of the audited system

## Maintainer

- [Nicolas GRELLETY](https://github.com/Nillyr)

## Authors

- [Nicolas GRELLETY](https://github.com/Nillyr)

## Copyright and license

Copyright (c) 2021-2022 Nicolas GRELLETY

This software is licensed under GNU GPLv3 license. See `LICENSE` file in the root folder of the project.

Icons made by [Smashicons](https://www.flaticon.com/authors/smashicons "Smashicons") from [www.flaticon.com](https://www.flaticon.com/ "Flaticon")
