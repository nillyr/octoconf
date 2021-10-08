# octoreconf

<p align="center">
  <img width="200" height="200" src="ressources/logo.png">
  <br/><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg">
  <img src="https://img.shields.io/badge/platform-macOS%2FLinux%2FWindows-blue.svg">
</p>

Tool dedicated to the realization of configuration audits of various systems via semi-automated analysis of the collected security configurations.

```
usage: octoreconf.py [-h] [-v] [-d] {analyze,audit,misc} ...

        ,'""`.       octoreconf v1.2.2b
       / _  _ \
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\
     (( ((  )) ))    /** Nicolas GRELLETY ( ngy.cs@protonmail.com ) **/
   hh `\ `)(' /'


positional arguments:
  {analyze,audit,misc}  Available Commands
    analyze             performs an analysis on an archive based on a checklist
    audit               performs an audit of the host based on a checklist
    misc                miscellaneous commands

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print version and exit
  -d, --debug           debug output (verbose)
```

## Quick usage

- Create your checklist based on the template
- Check the correct translation into JSON using the hjson tool (`hjson -j checklist.hjon`)
- Recommended: Assess the potential negative impact of the checklist on a test environment
- Perform an audit on the current system or an analysis on a collection

## Requirements

- Python 3.7+
- pip

## Installation

```
# On Linux and macOS
bash setup.sh
# On Windows
.\setup.bat
```

## Disclaimer

- This tool does not offer any guarantee
- The authors of this tool cannot be held responsible for the effects caused by the commands made in the checklists
- It is highly recommended to risk assess your checklists on a test virtual machine before using them in production
- It is highly recommended to manually check each critical configuration of the audited system

## Authors

- [Nicolas GRELLETY](https://github.com/Nillyr)

## Copyright

- Development based on the work done by [kristovatlas](https://github.com/kristovatlas/osx-config-check)

- Icons made by [Smashicons](https://www.flaticon.com/authors/smashicons "Smashicons") from [www.flaticon.com](https://www.flaticon.com/ "Flaticon")
