# octoreconf

<p align="center">
  <img width="200" height="200" src="ressources/logo.png">
  <br/><br/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/coverage-84%25-green.svg">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg">
  <img src="https://img.shields.io/badge/platform-macOS%2FLinux%2FWindows-blue.svg">
</p>

Tool dedicated to the realization of configuration audits of various systems via semi-automated analysis of the collected security configurations.

```
usage: octoreconf.py [-h] [-v] [-d] {analyze,audit,misc} ...

        ,'""`.       octoreconf v1.2.6b
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
- Recommended: Assess the potential negative impact of your checklist on a test environment
- Perform an audit on the current system or an analysis on a collection
  - The archive must have been made via the script that was produced by the script generation use case

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

## Use cases description

### Script Generation

- Input: a checklist
- Output: a collection script

This use case allows to generate from a checklist passed in argument a collection script in the chosen language (see the list of supported languages in the help output). It is also possible to generate collection scripts for devices such as routers, switches, etc. The Epilog and Prolog parts of the script may need to be modified.

#### Examples

```bash
# Linux
python octoreconf.py misc gen-script -c checklist.hjson -l bash -p linux -o linux-collection-script.sh
# macOS
python octoreconf.py misc gen-script -c checklist.hjson -l bash -p mac -o mac-collection-script.sh
# Windows (Batch)
python octoreconf.py misc gen-script -c checklist.hjson -l batch -p windows -o windows-collection-script.bat
# Windows (Powershell)
python octoreconf.py misc gen-script -c checklist.hjson -l powershell -p windows -o windows-collection-script.ps1
```

### Audit

- Input: a checklist
- Output: an XLSX and a JSON file

This use case allows to execute all the specified commands from a checklist. The results of the "collection_cmd" will be present in output files. The output path is automatically determined by taking into account the name of the category and the file specified in the command.

After the execution of the commands, the results are verified taking into account the verification type requested.

Finally, an XLSX file is generated presenting the results graphically. A JSON file is also generated for later use.

#### Examples

```bash
# Launch the audit
python octoreconf.py audit -c checklists.hjson -o ouput_dir/
# Launch the audit and specify the language to use in the output file (xlsx)
python octoreconf.py audit -c checklists.hjson -o ouput_dir/ -l en
```

### Analyze

- Input: a checklist and an archive
- Output: an XLSX and a JSON file

This use case allows an analysis of the results of the checks based on a checklist.

**Important:** the archive must have been generated by the collection script derived from the checklist used for the analysis.

#### Examples

```bash
# (tag.gz format) Launch the analyze
python octoreconf.py analyze -a archive.tar.gz -c checklist.hjson
# (tag.gz format) Launch the analyze and specify the language to use in the output file (xlsx)
python octoreconf.py analyze -a archive.tar.gz -c checklist.hjson -l en
# (zip format) Launch the analyze
python octoreconf.py analyze -a archive.zip -c checklist.hjson
# (zip format) Launch the analyze and specify the language to use in the output file (xlsx)
python octoreconf.py analyze -a archive.zip -c checklist.hjson -l en
```

### Report Generation

- Input: a JSON file
- Output: an XLSX and a JSON file

This use case can be called automatically as a chain of other use cases or independently. When called independently, this use case takes as input a JSON file (the one produced by the other use cases) in order to (re)generate a file in XLSX format.

#### Examples

```bash
# Launch the report generation
python octoreconf.py -d misc gen-report -i 20211006115003_results.json
# Launch the report generation and specify the language to use in the output file (xlsx)
python octoreconf.py -d misc gen-report -i 20211006115003_results.json -l en
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
