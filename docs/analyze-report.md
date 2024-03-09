# Analyze and generate reports

## Table of contents

- [Introduction](#introduction)
- [Basic usage](#basic-usage)
- [Report initialization](#report-initialization)
- [Introduction to report templates](#introduction-to-report-templates)
- [Create your own templates](#create-your-own-templates)
    - [Template](#template)
    - [Themes](#themes)
- [Audit the audit evidence and generate the reports with a template](#audit-the-audit-evidence-and-generate-the-reports-with-a-template)
- [Regenerate the report in PDF format](#regenerate-the-report-in-pdf-format)
- [MISC commands](#misc-commands)
    - [List available report templates](#list-available-report-templates)
    - [Import a report template](#import-a-report-template)
    - [Export your report templates](#export-your-report-templates)

## Introduction

The `analyze` command is used to analyze the audit evidence and generate the reports based on the selected baseline.

When using the `octowriter` submodule, a PDF and XLSX reports are generated. Moreover, a PDF template (see `pdf-theme` in `asciidoctor-pdf` documentation) can be used when generating the report. By default, only a CSV report is generated.

## Basic usage

Without any submodules, the `analyze` command can be used to generate a CSV report.

```bash
octoconf-cli analyze -b /path/to/baseline.yaml -a /path/to/audit_evidence.zip
```

## Report initialization

Scope: `octowriter` submodule

When using the `octowriter` submodule, a `.ini` file can be used to initialize the PDF report. See below an example of this file:

```ini
[DEFAULT]
# The auditee company name
auditee_name = Tricatel

# This paramater is not used by default (see next section for more information)
auditee_logo_path = /full/path/to/the/auditee/logo.png

# The recipient of the report
auditee_contact_full_name = Jacques Tricatel
auditee_contact_email = Jacques.Tricatel@tricatel.fr

# Your project manager
project_manager_full_name = Charles Duchemin
project_manager_email = Charles.Duchemin@guide-duchemin.fr

# You and your team
authors_list_full_name = Charles Duchemin; Gérard Duchemin
authors_list_email = Charles.Duchemin@guide-duchemin.fr; Gérard.Duchemin@guide-duchemin.fr

# What asset has been audited
audited_asset = canning-worker.tricatel.lan

# The classification level of the report
classification_level = Confidential

# Your company name
auditor_company_name = Guide Duchemin
```

When this file is not created, you will have to fill the information manually when generating the report.

Copyright: The information used in the "report information" configuration file come from the movie "[L'Aile ou la Cuisse](https://www.allocine.fr/film/fichefilm_gen_cfilm=47573.html)".

## Introduction to report templates

Scope: `octowriter` submodule (PDF report only)

| :information_source: Information |
|:---------------------------------|
| The word "template" is used. However, it's more a "theme" than a "template". Yet, it's possible to create a new `PDFGenerator` that implements the `IPDFGenerator` abstract class in order to create a real template that perfectly suits your needs. |

| :information_source: Information |
|:---------------------------------|
| By default, the `default` template and theme (included within the tool) is used. |

In order to generate the report, the tool uses `asciidoc` and `asciiidoctor-pdf`. As stated in the "install" documentation, `asciidoctor`, `asciidoctor-pdf` and `ruby-rouge` must be installed in order to use the `octowriter` submodule.

The template directory structure is as follows:

```text
.
├── custom                    # Custom templates directory where your templates are imported
└── default                   # Default templates directory
    ├── header.adoc           # This file contains all the information provided by the .ini file
    ├── introduction.adoc     # Standard introduction that contains the auditor's information as well as the auditee's information and the history of the report
    ├── resources             # This directory contains all the resources used in the report
    │   ├── images            # This directory contains all the images used in the report
    │   └── themes            # This directory contains all the themes available for the template
    │       └── default.yml   # This file contains the theme configuration
    └── synthesis.adoc        # This file contains the synthesis of all the non-compliant security controls
```

When using `asciidoctor-pdf`, the `default` directory is used for the parameter `--theme-dir` and the `default.yml` file is used for the parameter `--pdf-theme`.

The last section introduce the `auditee_logo_path` parameter. This parameter is used to add the auditee's logo in the report. When this parameter is used, the auditee's logo will be imported in the "images" directory of the choosen template.

| :information_source: Information |
|:---------------------------------|
| The `default.yml` theme **does not** use this paramater. Even if it's set, no images will be added to the report. |

## Create your own templates and themes

### Template

If you want to create a new template and not just custom the theme, you will have create your own `PDFGenerator` class that implements the `IPDFGenerator` abstract class. The following snippet gives you the base structure of the class:

```python
import configparser

from octoconf.interfaces.generate_pdf import IPDFGenerator

class PDFGenerator(IPDFGenerator):
    def __init__(self, ...) -> None:
        # Your code here
        pass

    def build_pdf(self, ...) -> None:
        # Your code here
        pass

    def generate_pdf(self, ...) -> None:
        # Your code here
        pass
```

### Themes

The theme of the PDF can be customized following the [Asciidoctor PDF Theming documentation](https://docs.asciidoctor.org/pdf-converter/latest/theme/).

| :bulb: Tips |
|:------------|
| If you only have one theme, name the file `default.yml` and you will not have to add this parameter anymore. |

## Audit the audit evidence and generate the reports with a template 

The following command allows the user to analyze the audit evidence and generate the reports based on the default template:

```bash
octoconf-cli analyze \
    -b /path/to/baseline.yaml \
    -a /path/to/audit_evidence.zip \
    -o "`pwd`/reports/" \
    --ini /path/to/ini_file.ini
```

In order to use a custom theme, the following command can be used:

```bash
octoconf-cli analyze \
    -b /path/to/baseline.yaml \
    -a /path/to/audit_evidence.zip \
    -o "`pwd`/reports/" \
    --ini /path/to/ini_file.ini \
    --theme-dir theme_directory \
    --pdf-theme theme_name.yml
```

See also: [List available report templates](#list-available-report-templates)

## Regenerate the report in PDF format

When editing the `.adoc` file, you will have to regenerate the PDF report. The following command allows the user to regenerate the PDF report based on a custom template:

```bash
octoconf-cli report \
    -i /path/to/build/adoc/header.adoc \
    -o "`pwd`/reports/" \
    --theme-dir theme_directory \
    --pdf-theme theme_name.yml
```

## MISC commands

The commands below are not part of the standard usage of the tool. They are used to manage the templates.

### List available report templates

The following command allows the user to list available templates:

```bash
octoconf-cli template list 
```

Sample output:

```text
Themes directory        Themes                  Source
----------------------- ----------------------- -----------
default                 default.yml             Built-in
```

### Import a report template

Note: `octowriter` submodule must be used in order to import a report template.

The following command allows the user to import an archive (ZIP) with custom templates. The `--action` option is used to specify the action to perform. The default action is `merge`.

The `merge` action will add the new templates and update the existing one. The `replace` action will **completely delete** the existing custom templates and extract the archive. The default value is `merge`.

```bash
# Default action: merge
## This command:
octoconf-cli template import -a /path/to/archive.zip
## Is the same as this one:
octoconf-cli template import -a /path/to/archive.zip --action merge

# Overwrite existing baselines
octoconf-cli template import -a /path/to/archive.zip --action replace
```

### Export your report templates

Note: `octowriter` submodule must be used in order to export a report template.

The following command allows the user to export **only your custom templates** into an archive (ZIP). The archive is created in the current working directory.

```bash
octoconf-cli template export
```

