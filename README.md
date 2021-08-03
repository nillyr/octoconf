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

## Disclaimer

- This tool does not offer any guarantee
- No responsibility can be taken for the effects potentially caused by the commands made in the checklists
- It is highly recommended to risk assess your checklists on a test virtual machine before using them in production
- It is highly recommended to manually check each critical configuration of the audited system

## How-to

from inside the virtual env
Check your checklist

```bash
hjson -j checklist.hjson
```

## Requirements

- Python3.7+
- PIP

## Installation

- On macOS and Linux

```bash
bash setup.sh
```

- On Windows

```batch
.\setup.bat
```

## Usage

```
usage: octoreconf.py [-h] [-v] [-d] [--audit CHECKLIST] [--regen-report JSON]
                     [--analyze CHECKLIST ARCHIVE]

        ,'""`.       octoreconf v1.0.0b
       / _  _ \ 
       |(@)(@)|      Tool for semi-automatic verification
       )  __  (      of security configurations.
      /,'))((`.\
     (( ((  )) ))    /** Nicolas GRELLETY ( ngy.cs@protonmail.com ) **/
   hh `\ `)(' /'
  

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print version
  -d, --debug           debug output (verbose)
  --audit CHECKLIST     runs an audit on the current system using a checklist
  --regen-report JSON   regenerate a report based on a JSON output file
                        provided by the 'audit' option
  --analyze CHECKLIST ARCHIVE
                        runs an analysis based on a checklist and an archive
                        (zip) containing all the configurations
```

## Copyright

- Development based on the work done by [kristovatlas](https://github.com/kristovatlas/osx-config-check)

- Icons made by [Smashicons](https://www.flaticon.com/authors/smashicons "Smashicons") from [www.flaticon.com](https://www.flaticon.com/ "Flaticon")
