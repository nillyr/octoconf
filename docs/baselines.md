# Baselines management and usage

## Table of contents 

- [Introduction](#introduction)
- [Baseline structure](#baseline-structure)
    - [Baseline content](#baseline-content)
    - [Rule content](#rule-content)
- [Scoping and Tailoring](#scoping-and-tailoring)
- [Package your baseline for import](#package-your-baseline-for-import)
- [Standard usage](#standard-usage)
    - [Generate a collection script](#generate-a-collection-script)
- [MISC commands](#misc-commands)
    - [List available baselines](#list-available-baselines)
    - [Import your baselines](#import-your-baselines)
    - [Export your baselines](#export-your-baselines)
    - [Translate a baseline](#translate-a-baseline)

## Introduction

Security baselines are the core of the tool. They are used to generate the collection scripts and the reports.

## Baseline structure

When creating a baseline, the following structure is required:

```text
Directory: baselines/{baselines,custom}/<baseline_name>/

.
├── baseline_name.yaml              # This is the baseline you will use to generate the collection script
└── rules                           # This directory contains the rules (1 control = 1 file)
    ├── rule_file_name_1.yaml
    ├── rule_file_name_2.yaml
    ├── ...
    └── rule_file_name_n.yaml
```

| :information_source: Information |
|:---------------------------------|
| There are no requirements on file names. Moreover, both `.yaml` and `.yml` extensions can be used. |

| :warning: Warning |
|:---------------------------------|
| If the same file exists with the extensions `.yaml` and `.yml`, only the first file found will be used. |

### Baseline content

The baseline is a YAML file that contains the following fields (example with only one category):

```yaml
title: "The title of the baseline (example: Debian GNU/Linux server v1.0)"
categories:
  # The category name must be unique and without spaces
  - category: a_category_name
    name: A category name
    description: |
        A description of the category.
    # The rules are listed in the order they will appear in the report
    # The rule_file_name is the name of the file without the extension
    rules:
      - rule_file_name_1
      - rule_file_name_2
      - ...
      - rule_file_name_n
```

### Rule content

The rule is a YAML file in the `rules` directory that contains the following fields:

```yaml
# The rule ID must be the same as the file name but without the extension
id: rule_file_name
title: The title of the rule
description: |
  A description of the rule.
  What is the benefit of this configuration? What is the risk if the configuration is not applied?

# The collection_cmd is used to collect some evidence in order to manually check the result later.
# The syntax is the following:
# <command> <redirector> <output_file> [; <command> <redirector> <output_file>]
# You can also have one command per line:
# <command> <redirectort> <output_file>

# IMPORTANT: do not specify the output directory because this one is automatically added by the tool.
# cmd > file.txt becomes cmd > basedir/category/file.txt

# Note: the available redirectors are listed in the following files:
# - octoconf/interface_adapters/redirector_regex/unix_output_redirector_regex_concrete_builder.py
# - octoconf/interface_adapters/redirector_regex/windows_output_redirector_regex_concrete_builder.py

# If your redirector is not matched by the regex, open an issue or create a PR.
collection_cmd: |
  arch > arch_output.txt

# This section contains the commands to be used to automatically check that the configuration is compliant.
# The following example checks if the architecture is 64-bit:
check: |
  # The full line of '#' is not needed, it is just to separate the different parts of the script
  ################################################################################
  LANG=en_US.utf8

  RULE_ID="rule_file_name"
  HOSTNAME="$(hostname -f)"
  DATE="$(date +"%Y/%m/%d")"

  STATUS=RESULT_CHECK_FAIL

  arch | grep -q -E "x86_64|amd64|aarch64" && STATUS=RESULT_CHECK_PASS

  # You must not redirect the output to a file
  # This is done automatically when the collection script is generated
  printf "RULE_ID: %s\nHOSTNAME: %s\nDATE: %s\n\n%s\n" "${RULE_ID}" "${HOSTNAME}" "${DATE}" "${STATUS}"

# verification_type:
# - CHECK_REGEX: there must be a match between the output and the expected result (case insensitive)
# - CHECK_EXACT: output == expected
verification_type: CHECK_REGEX
expected: ^\s*RESULT_CHECK_PASS
recommendation: |
  Description of the recommendation.
  What should be done to apply the configuration?
  What are the consequences of applying the configuration?
  What is the difficulty/cost ratio required to process the recommendation.
  When possible, provide a link to a documentation or a guide.
  When possible, provide a command (or playbook / role when using tools like Ansible) to apply the recommendation.

  If you want to provide a command, a script, a snippet, etc., you have to use the following syntax (required by asciidoctor). Example: disable ssh root login with Ansible playbook:

  [source%linenums,yaml]
  [options="nowrap"]
  ----
  - name: Disable SSH Root Login
    hosts: all
    become: true

    ansible.builtin.lineinfile:
      path: "{{ item }}"
      regexp: "^\s*PermitRootLogin"
      line: "PermitRootLogin no"
    with_items:
      - /etc/ssh/sshd_config
    notify:
      - Restart SSH service

    handlers:
      - name: Restart SSH service
        become: true
        ansible.builtin.service:
          name: ssh
          state: restarted
  ----

  See: https://docs.asciidoctor.org/asciidoc/latest/verbatim/source-blocks/ for more information

# The level of the rule (default: minimal)
# The possible values are:
# - minimal       -> Basic recommendation to be implemented systematically on all systems
# - intermediary  -> To be implemented as soon as possible on most systems
# - enhanced      -> For use on systems with high security requirements, or where several applications applications to be isolated from each other on the same system
# - high          -> To be implemented if and only if in-house resources have the skills and time required to maintain them on a regular basis. These can, however, bring a significant security gain.
level: minimal 

# Any references that can be used to justify the rule (CIS, NIST, ANSSI, etc.).
references:
  - a_reference_or_a_link
```

| :information_source: Information |
|:---------------------------------|
| The example has been written for a GNU/Linux system. Therefore, Bash commands are used. Obvisouly, for Windows, PowerShell will be used. |

## Scoping and Tailoring

- Scoping: edit the `baseline_name.yaml` to comment security controls that are not applicable.
- Tailoring: edit the rules in the `rules` directory.

If the cutomization need to be done on a built-in baseline, head to [octobaselines](https://github.com/nillyr/octobaselines) repository and download the baseline you need. Then, follow the instructions in the [Package your baseline for import](#package-your-baseline-for-import) section.

| :information_source: Information |
|:---------------------------------|
| Each baseline must be unique. You will have to change the baseline's title or the baseline's filename. See [List available baselines](#list-available-baselines). |

## Package your baseline for import

To import your custom baselines, you must package them into a ZIP file. The ZIP file must have the following structure:

```text
custom
└── your_baselines_collection       # You can collapse in one directory level this directory
    └── your_baseline_shortname     # And this one
        ├── your_baseline.yaml
        └── rules
            ├── your_rule_id_1.yaml
            ├── your_rule_id_2.yaml
            ├── ... 
            └── your_rule_id_n.yaml
```

Now jump to the [Import your baselines](#import-your-baselines) section to see how to import your custom baselines.

## Standard usage

### Generate a collection script

The following command allows the user to generate a collection script from a baseline. The `-b` option is used to specify the baseline to use. The `-o` option is used to specify the output file. The `-p` option is used to specify the targeted platform. The `-u` option is used to specify the path to your utility script containing the functions used in your baseline, which should be included in the generated script. Note: this option should only be used when using your own baselines.

The available platforms are `linux`, `mac` and `windows`.

```bash
# Generate a collection script
octoconf-cli baseline generate_script \
    -p linux \
    -b /path/to/baseline.yaml \
    -o /path/to/output_script.sh

# Generate a collection script with utils functions included
octoconf-cli baseline generate_script \
    -p linux \
    -b /path/to/baseline.yaml \
    -u /path/to/utils_script.sh \
    -o /path/to/output_script.sh
```

When using utils script and `bash` language, the script must not containt the `#!/bin/bash` line. If you use [shellcheck](https://github.com/koalaman/shellcheck), add the following line at the beginning of the script:

```bash
# shellcheck shell=bash
```

## MISC commands

The commands below are not part of the standard usage of the tool. They are used to manage the baselines.

### List available baselines

The following command allows the user to list available baselines:

```bash
octoconf-cli baseline list
```

Sample output: 

```text
# When no baselines are available
No entry found

# When baselines are available (either Built-in or Custom)
Title                                        Filename                      Source
-------------------------------------------- ----------------------------- -----------
Audit de sécurité d'un serveur GNU/Linux     generic_linux_server.yaml     Built-in
```

To use available baselines, you do not have to use the baseline's path. You can use either the baseline's title or the baseline's filename. The tool will automatically find the baseline. This is true for `generate_script` and `analyze` commands.

Exemple:

```bash
# Use the baseline's title
octoconf-cli baseline generate_script \
    -p linux \
    -b "Audit de sécurité d'un serveur GNU/Linux" \
    -o /path/to/output_script.sh

# Use the baseline's filename 
octoconf-cli baseline generate_script \
    -p linux \
    -b generic_linux_server.yaml \
    -o /path/to/output_script.sh
```

### Import your baselines

The following command allows the user to import an archive (ZIP) with custom baselines. The `--action` option is used to specify the action to perform. The default action is `merge`.

The `merge` action will add the new baselines and update the existing one. The `replace` action will **completely delete** the existing custom baselines and extract the archive. The default value is `merge`.

```bash
# Default action: merge
## This command:
octoconf-cli baseline import -a /path/to/archive.zip
## Is the same as this one:
octoconf-cli baseline import -a /path/to/archive.zip --action merge

# Overwrite existing baselines
octoconf-cli baseline import -a /path/to/archive.zip --action replace
```

### Export your baselines

The following command allows the user to export **only your custom baselines** into an archive (ZIP). The archive is created in the current working directory.

```bash
octoconf-cli baseline export
```

### Translate a baseline

Prerequisites: you must have define your `API_KEY` in your configuration file (see [Configuration management](configuration.md) and [Where can I find my Authentication Key?](https://support.deepl.com/hc/en-us/articles/360020695820-Authentication-Key) for more information).

The following command allows the user to translate a baseline. The `-s` and `-t` options are used to specify the source and target languages. The `-o` option is used to specify the output directory.

```bash
octoconf-cli baseline translate \
    -b /path/to/baseline.yaml \
    -o /path/to/output/directory/ \
    -s <source_lang> \
    -t <target_language>
```

| :information_source: Information |
|:---------------------------------|
| To reduce API usage, translations are cached (located at `$HOME/.cache/octoconf/` for GNU/Linux and macOS and at `C:\Users\<user>\AppData\Local\octoconf\cache\` for Windows). So when the message to be translated is cached, the stored value is used directly, without going through the API. |

| :bulb: Tips |
|:------------|
| Modify cached translated values to customize your translations. |

| :information_source: Information |
|:---------------------------------|
| Some language pairs are not supported by DeepL. See [Supported Language Pairs](https://www.deepl.com/docs-api/glossaries/list-glossary-languages) |

