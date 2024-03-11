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
</p>

Tool dedicated to the realization of configuration audits.

```text
        ,'""`.       octoconf 2.4.0-beta
       / _  _ \
       |(@)(@)|      Tool dedicated to the realization
       )  __  (      of configuration audits.
      /,'))((`.\
     (( ((  )) ))    /** @nillyr **/
   hh `\ `)(' /'


positional arguments:
  {analyze,baseline,report,config}
                        Available Commands
    analyze             performs an analysis on an archive based on a security baseline
    baseline            performs the interaction with the security baselines
    util                performs the interaction with the utility scripts
    report              performs the recompilation of the report in PDF format from an adoc file
    template            performs the interaction with your custom report templates
    config              performs octoconf configuration management

options:
  -h, --help            show this help message and exit
  --version             print version and exit
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        set the log level (default: INFO)
```

## Table of contents

- [Disclaimer](#disclaimer)
- [Standard usage](#standard-usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Copyright and license](#copyright-and-license)

## Disclaimer

- This is not a turn key tool, read the documentation for more information;
- This tool does not offer any guarantee;
- The authors of this tool cannot be held responsible for the effects caused by the executed commands;
- It is highly recommended to risk assess your commands in a test environment before using them in production;
- It is highly recommended that the risk of service degradation be graded before any use on a system in production.

## Standard usage

1. Use a built-in baseline or create your own
2. Generate a collection script from the selected baseline 
3. Run the collection script on the target host
4. Analyze the results and generate the reports with or without your own report template
5. When required, edit the report and recompile it in PDF format

## Documentation

- [Install octoconf](docs/install.md)
- [Configure octoconf](docs/configuration.md)
- [Baselines management and usage](docs/baselines.md)
- [Analyze and generate reports](docs/analyze-report.md)

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md).

## Copyright and license

Copyright (c) 2021 Nicolas GRELLETY

This software is licensed under GNU GPLv3 license. See `LICENSE` file in the root folder of the project.

The information used in the "report information" configuration file come from the movie "[L'Aile ou la Cuisse](https://www.allocine.fr/film/fichefilm_gen_cfilm=47573.html)".

Icons made by [Freepik](https://www.flaticon.com/authors/freepik "Freepik") from [www.flaticon.com](https://www.flaticon.com/ "Flaticon")

