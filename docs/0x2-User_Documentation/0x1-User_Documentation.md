# User documentation

Many thanks for using the octoreconf tool and for taking the time to read its documentation. The following sections will help you to familiarise yourself with the tool from installation to generating audit reports.

## User installation

Two installation methods of the tool are available.

From the "compiled" version (recommended):

```bash
# Get the latest version of the tool at https://github.com/Nillyr/octoreconf/releases
python3 -m venv octoreconf
# Activate the venv
# Install wheel
python -m pip install octoreconf-<version>.whl
# or
python -m pip install octoreconf-<version>.tar.gz
```

Directly from the sources. This method is presented in section [developer installation](#developer-installation).

## Existing checklists

The tool uses the [octoreconf-checklists](https://github.com/Nillyr/octoreconf-checklists) submodule containing a set of checklists.

The existing checklists can be listed as follows:

```bash
# No filter
octoreconf checklist list
# Filter on desktop category
octoreconf checklist list -c desktop
```

## Creating the checklists

The format chosen for the checklists is hjson (human readable json).

### Checklist template

The basic template is as follows:

```bash
[
  {
    categories: [
      {
        # id must be int and unique
        id: 1
        name: A category
        checkpoints: [
          {
            # id must be int and unique
            id: 1
            # The title will be used in the generated files
            title: This is a title
            description:
            '''
            This is a
            multiline description.
            '''
            # Optionnal value. Should be an URL
            reference: https://www.my-reference.com/
            # Optionnal value
            # Performing a full extraction is highly recommended for collecting audit proof.
            /**
            * Optionnal value
            * Performing a full extraction is highly recommended for collecting audit proof.
            *
            * The output path must not be specified. The latter is automatically generated.
            *
            * Possible redirects:
            * - >
            * - >>
            * - | Out-File -Encoding utf8 -FilePath
            * - | Out-File -Encoding utf8 -Append -FilePath
            * - /H (gpresult.exe) or /cfg (SecEdit.exe)
            *
            * Need more? Create an issue.
            */
            collection_cmd: "<your command> <your_redirection> <output_file.ext>"
            # Optionnal value (must be present if collection_cmd is defined)
            # CMD_EXEC = /bin/bash
            # AUDIT_POWERSHELL = powershell.exe
            # BATCH_EXEC = cmd.exe
            collection_cmd_type: CMD_EXEC
            # Possible values: true | false
            # true: checks can be remove
            # false: checks must be defined
            collect_only: false
            checks: [
              {
                # id must be int and unique
                id: 1
                description: A short description
                # type:
                # CMD_EXEC = /bin/bash
                # AUDIT_POWERSHELL = powershell.exe
                # BATCH_EXEC = cmd.exe
                type: CMD_EXEC
                # No output file (it is done dynamically)
                cmd: "your_command"
                expected: "expected_value"
                /**
                * Type of verification to be performed
                * Possible values:
                *  - CHECK_EXACT   expects a simple value
                *  - CHECK_REGEX   expects a python regular expression
                */
                verification_type: CHECK_EXACT
                /**
                * Possible values:
                *  - high
                *  - medium
                *  - low
                *  - info
                */
                severity: high
                recommandation_on_failed:
                '''
                When the outcome is not what was expected, it is possible to print a recommendation.
                The recommendation may contain, among other things, the command for correction.
                '''
                # Optional value. String (multiline possible)
                see_also: https://www.my-reference.com/
              }
            ]
          }
        ]
      }
    ]
  }
]
```

### Checklist example

Below is an example of a category for Windows 10:

```bash
[
  {
    categories: [
        {
        id: 1
        name: Low level
        checkpoints: [
          {
            id: 1
            title: Bitlocker status
            description: Checking the status of Bitlocker
            collection_cmd: "manage-bde -status | Out-File -Encoding utf8 -Append -FilePath bitlocker_status.txt"
            collection_cmd_type: AUDIT_POWERSHELL
            collect_only: false
            checks: [
                {
                id: 1
                description: All disks encrypted
                type: AUDIT_POWERSHELL
                cmd: "$($volumes = Get-BitLockerVolume; If ($volumes | Where {$_.ProtectionStatus -ne 'On'}) { 'Some disks are not encrypted' } Else { 'All disks are encrypted' })"
                expected: "All disks are encrypted"
                verification_type: CHECK_EXACT
                severity: medium
                recommandation_on_failed:
                '''
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sit amet nunc varius dolor fermentum pulvinar. Proin dignissim semper condimentum. Nam quis maximus elit.
                '''
              },
            ]
          },
        }
      ]
    ]
  }
]
```

## User workflows

### Audit

Allows to execute all the specified commands from a checklist. The results of the "collection_cmd" will be present in output files. The output path is automatically determined by taking into account the name of the category and the file specified in the command.

After the execution of the commands, the results are verified taking into account the verification type requested.

Finally, an XLSX file is generated presenting the results graphically. A JSON file is also generated for later use.

![Figure 2-1: User workflows - Audit](docs/figures/user-workflows-audit.png)

#### Command examples: Audit

```bash
# Launch the audit
octoreconf audit -c checklists.hjson -o ouput_dir/
# Launch the audit and specify the language to use in the output file (xlsx)
octoreconf audit -c checklists.hjson -o ouput_dir/ -l en
```

### Analyze

Allows an analysis of the results of the checks based on a checklist.

**Important:** the archive must have been generated by the collection script derived from the checklist used for the analysis.

![Figure 2-2: User workflows - Analyze](docs/figures/user-workflows-analyze.png)

#### Command examples: Analyze

```bash
# (tag.gz format) Launch the analyze
octoreconf analyze -a archive.tar.gz -c checklist.hjson
# (tag.gz format) Launch the analyze and specify the language to use in the output file (xlsx)
octoreconf analyze -a archive.tar.gz -c checklist.hjson -l en
# (zip format) Launch the analyze
octoreconf analyze -a archive.zip -c checklist.hjson
# (zip format) Launch the analyze and specify the language to use in the output file (xlsx)
octoreconf analyze -a archive.zip -c checklist.hjson -l en
```

### Script generation

Allows to generate from a checklist passed in argument a collection script in the chosen language (see the list of supported languages in the help output). It is also possible to generate collection scripts for devices such as routers, switches, etc. The Epilog and Prolog parts of the script may need to be modified.

![Figure 2-3: User workflows - Script generation](docs/figures/user-workflows-script_generation.png)

#### Command examples: Script generation

```bash
# Linux
octoreconf checklist generate -c desktop/ubuntu20-04 -l bash -p linux -o ubuntu20-04.sh
# macOS
octoreconf checklist generate -c desktop/macOS11 -l bash -p mac -o macOS11.sh
# Windows (Batch)
octoreconf checklist generate -c desktop/windows10 -l batch -p windows -o windows10.bat
# Windows (Powershell)
octoreconf checklist generate -c desktop/windows10 -l powershell -p windows -o windows10.ps1
```

### Report generation

This use case can be called automatically as a chain of other use cases or independently. When called independently, this use case takes as input a JSON file (the one produced by the other use cases) in order to (re)generate a file in XLSX format.

![Figure 2-2: User workflows - Report generation](docs/figures/user-workflows-report_generation.png)

#### Command examples: Report generation

```bash
# Launch the report generation
octoreconf report -i 20211006115003_results.json
# Launch the report generation and specify the language to use in the output file
octoreconf report -i 20211006115003_results.json -l en
```
