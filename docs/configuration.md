# Configuration management 

## Table of contents

- [Introduction](#introduction)
- [Print the current configuration](#print-the-current-configuration)
- [Edit the configuration](#edit-the-configuration)

## Introduction

The `config` command allows the user to manage the configuration of octoconf. Most of the parameters are used for the `XLSX` (language, colors and classification) and `PDF` (language only) reports generation.

The configuration file is located at `$HOME/.config/octoconf/octoconf.ini` on GNU/Linux and macOS and at `C:\Users\<user>\AppData\Local\octoconf\octoconf.ini` on Windows.

## Print the current configuration

To print the current configuration, use the `print` command:

```bash
octoconf-cli config print
```

## Edit the configuration

To edit the configuration, use the `edit` command:

```bash
octoconf-cli config edit -s <section> -o <option> -v <value>
```

For example, if you want to set your `API_KEY` for DeepL, you can use the following command:

```bash
octoconf-cli config edit -s translator -o deepl_api_key -v <your_api_key>
```

