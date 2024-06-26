# Changelog

<a name="2.1.0-beta"></a>
## 2.1.0-beta (2023-08-06)

### Added

- 🔊 add logging [e95c356]
- 👷‍♂️ update CI system [9fcc655]
- ✨ add gitmoji-changelog spec [9569799]
- ✨ add a util script [dfe9a20]
- 👷‍♂️ update gitlab ci config [588bffa]
- 👷‍♂️ testing gitlab-ci config [84fcab2]
    * 👷‍♂️ testing gitlab-ci config (0bf3782)
    * 👷‍♂️ testing gitlab-ci config (17c94b4)
    * 👷‍♂️ testing gitlab-ci config (696ed06)
- ✅ fix unit tests [f4508e1]
    * ✅ unit test fix (ffc358e)
- ✨ added automatic generation of the pdf report [80f85a9]
- ✅ add unit test for regex [f46f12b]
- ✅ update existing unit tests [ddcf1da]
- ✨ added functionality to manage the configuration of the tool [52f0c39]
- ✨ added the configuration value &#x27;language&#x27; for various actions [76cdeff]
- ✨ adding powershell command chaining [f45a056]
- ✨ added the possibility to combine commands when collecting configuration (e.g. cmd_a &gt; output_1.txt; cmd_b &gt; output_2.txt) [2fea840]
- ✨ add level notion on checks [d8b4823]
- ✨ add yml extension support [65fc969]
- ➕ add wheel dependency in dev requirements [4659bd3]
- 👷‍♂️ ci: specify severity threshold [317a537]
- 👷‍♂️ ci: add snyk workflow [baf008f]
- 👷‍♂️ ci: add macos-latest os [546cc70]
- 👷‍♂️ update trigger events [0783ea0]
    * 👷‍♂️ ci: update trigger events (0a0206a)
- 👷‍♂️ ci: fix trigger events [e4949a2]
- 👷‍♂️ ci: update workflow [3335851]
- 👷‍♂️ buid: add github action to run tests [456a6b5]
- ✨ feat: added configuration feature [4d5cc6a]
- ➕ Add a dependency [fcfccfb]
- 👷‍♂️ Update makefile [8eef00f]
- ➕ Added yaml dependency [a25a10b]
- ✨ Added Export-CSV cmdlet regex [fb31550]
- ✨ Creation of a simplistic cache system to limit the number of requests to the translator [e2c8368]
- ✨ Implemented the use case for checklist translation [a1a1456]
- ✨ Added tee-object cmdlet regex [4c191d3]
- ✨ Added xml report generation [2d92f11]
- ✨ Added checklist export (issue #5) [41b8418]
- ✨ Replacement of the checklist by the corresponding path [157a6a0]
- ✨ Added functionality to list loaded checklists [02e31b9]
    * ✨ Added functionality to load submodule checklists (821aebe)
- ✅ Updated unit tests [4c4c693]
    * ✅ Updated unit tests (00cc873)
- ✨ Added some switches to redirect output to files [aeec3e0]
- ✨ Added a line to be completed in the generated report [0e04c1b]
- ✅ Added some tests [68273f9]
- ✨ Added the possibility of making a collection without making checks. [9f17188]
- ➕ Added a submodule to manage the different checklists [5d485fd]
- ✨ Added the severity level on the checks [2df5b41]
- ✅ Added some tests and increase coverage [d265cb8]
- ✅ Added unit tests on the generation of the collection script [d2cd32a]
- ✅ Addition of unit tests concerning checker and script generator [4a33fdc]
- ✅ Addition of unit tests concerning encoders and correction of a bug. [d963bf7]
- ✅ Addition of tests for entities initialization [e29697b]
- ✨ Excel reporting is now available [fecf06b]
- ✨ Analyze use case is now available [af4bb73]
- ✨ Audit - Check output is now available with exact and regex match [82098ba]
- ✨ Audit - Checks runner is now available [c01b022]
- ✨ Collection Script Generator (powershell) for windows platform done [f714c9d]
    * ✨ Collection Script Generator (batch) for windows platform done (c08462b)
- ✨ Collection Script Generator for linux platform done [cc9da9c]
    * ✨ Collection Script Generator for macOS platform done (9d520a5)
- ✨ Rework args parser to introduce new features [ec07c29]
- ✨ Add a checklist parser [7533b97]
- ➕ Adding dependency [81e5135]
- ✨ Adding automatic environment initialization on Windows [d9a1a22]
    * ✨ Adding automatic environment initialization (e911575)
- 🎉 Init Readme.md file [9f50a80]

### Changed

- 🏗️ update build configuration [74ae468]
    * 👷‍♂️ update ci configuration (ea0e52a)
- 🎨 black formatter [157e4c9]
    * 🎨 Run black formatter (ae3298d)
- 🔧 update vscode configuration [f752625]
- 🚚 move unittest folder and update related conf [d9342cc]
- 🔧 move application data [535ee8b]
- 🍱 update themes [a102ea0]
- 🚸 improve user exp [5919700]
- ⬆️ upgrade dependencies [c96fb36]
    * ⬆️ upgrade dependencies (1b12929)
    * ⬆️ upgrade dependencies (dcc79bc)
    * ⬆️ upgrade dependencies (4d0a83b)
- 💄 add property information for pdf report [12406ca]
- 🚚 rename resources [96d3ba6]
- 🚸 improving the user experience [5f66520]
- 🍱 update issue templates labels [b8107e7]
- 💄 update usage message [89dd9bd]
- 🎨 modify the use of the translation feature [cdae941]
- 🔧 update Makefile actions [55635c0]
- 🚚 update imports [2faf701]
- 🔧 edit vscode settings [68f3102]
- 🎨 improve script generation [678b817]
    * ⚡ improve regex for script generation (c1e5e00)
    * 🎨 improve collection script (8df8482)
    * 🎨 improve collection script (d46955d)
    * 🎨 improve collection script (19740e4)
- 🎨 update script generation and related unit tests [c120128]
- 🎨 update script generation [2dcf9a0]
- 🎨 improve generated xlsx report [59cb8e8]
- 🎨 edit configuration management of the tool [fb267c9]
- 💬 update translation [b47c681]
- 🎨 improved quality of Excel report [e53bba5]
- 💬 add classification levels [34cbb6d]
    * 💬 add classification levels (98798e5)
- 🚨 update pytest filtering [73d8db5]
- 🎨 improve collection script generation [04ff66f]
    * 🎨 improve bash collection script decorator (81151b5)
- 🎨 improved quality of the generated Excel report [790f3a4]
- 🎨 modification of the generation of collection scripts [5473bae]
    * 🎨 modification of the generation of collection scripts (a422220)
- 💬 add translation [b4d1936]
- 🎨 edit script and report generation [6136bd9]
- 🚚 move output directory [1eca406]
- 🎨 edited generated report information sheet [0db354e]
- 🎨 finetuning the collection script [5e0a4a7]
    * 🎨 finetuning the collection script (2501276)
    * 🎨 finetuning the collection script for macos (e657fb2)
    * 🎨 finetuning the collection script for macos (99a6aaf)
- 🎨 added a sheet containing general information [112aaa8]
- 🎨 redesign of the report generation [785a57c]
- 🎨 finetuning the collection script for macos and gnu/linux [d56128f]
    * 🎨 finetuning the collection script for gnu/linux (ee560b8)
- 💬 redirect stderr to a given file [7af488f]
- 💬 update error message and fix a simple issue on bash script generation [d4c877a]
- ⏪ experimentation failed on windows -&gt; rewind to the last working version [b519de9]
- 💬 update literals to specify gnu/linux and not only the linux kernel [a265613]
- 🎨 simplification of script generation options [14a8a1c]
- 🎨 improve excel report generation [0b4f014]
- 🎨 improved excel report generation with support of formulas [f9616d0]
- 👽 migration from os.path to pathlib module [17167ee]
- 🚨 fix invalid escape sequence warnings in regex [4087e18]
- 🎨 remove trailing carriage return on cmd runner [93e502d]
- ♻️ change use case worflow [7ca7ef3]
- 🔧 normalizes the version by deleting the last carriage return [3956f78]
- ⚡ perf: improve perf [aa4aebc]
- ♻️ refactor: update configuration module [7d98d88]
- 🎨 style: edit xml output settings [057fb2c]
- 🔧 build: update setup scripts [5c6f542]
- ⬆️ build: python minimum version change [4252244]
- 🔧 Update vscode configuration files [90bf865]
    * 🔧 Adding some configuration files (ff7e038)
- 🚚 Renaming some stuff [5ba4f46]
- 🚚 Renaming resources... [8efb169]
    * 🚚 Renaming resources... (72daf35)
- 🏗️ Made some architectural changes [eac9f3b]
- ⬆️ Update checklist submodule [89fdef6]
- ⬆️ Updated dependencies [55c0c43]
- 👽 Edited the checklist template to add a title to the checks [7054c63]
- 🚚 Moved some files to keep the coherence on the whole project [0c35d43]
- 🎨 Modification of the xml output [e6dbbd5]
- ⚡ Improved combine redirection regex [650a927]
- ⚡ Improved out-file cmdlet regex [e6c7b65]
- 🏗️ Made some structural modifications in order to have only one place for the creation of the regex with all the redirections [dc13b48]
- 🏗️ Made some architectural changes on command exec [16bad89]
- 🚨 Turned warnings to errors [6b3de1d]
- 🎨 Added &#x27;info&#x27; severity level [7964a63]
- 🚚 Moved the checklist template to the submodule [054d1c6]
- 💬 Addition of some prints to reassure the user that the process is running smoothly [1630632]
- 🏗️ Realization of numerous architectural modifications [4c75588]
    * 🏗️ Realization of numerous architectural modifications (81590c0)
- 💬 Adding the copyright in the generated scripts [26d8aea]
- ⚡ Improving output directory management [8f9563e]
- 🎨 Improve generated script for final user experience [bdabe60]
- 🎨 Add code formatter [35a16ae]
- 🚨 Fix warnings [b8ab7d4]
- 🎨 Revamp args parser [81396b8]
- 🏗️ Project re-structuring part. 2 [eb7df26]
- 🏗️ Add the use of adapters [73637b3]
- 🎨 Improving structure [76d1612]
- 🚚 Renaming variables [b9cb90e]
- 🎨 Little simplification [7407bf5]
- 🏗️ Making some changes here and there... [e67b9ea]
- 🔧 Defining a checklist template [b2fcb9f]

### Breaking changes

- 💥 Switching from hjson to yaml checklists [19f16d9]
- 💥 Project Restructuring [9decb2f]
    * 🏗️ Project re-structuring (15e1a93)
- 💥 Support for powershell generated checks (encoding) and debugging [010212d]

### Removed

- ➖ remove unused dependency [f913869]
- 🔥 deleted severity notion and keep level only [fadc23d]
- 🔥 deleted support for the batch language [383720d]
- 🔇 Remove some debug output [be1d920]
- 🔥 Remove useless code [0631486]
- ➖ Remove a dependency [a4c37a5]
- 🔥 Remove optional output file argument [48130a0]
- 🔥 Removing old template [7f69ef2]

### Fixed

- 🐛 fix broken formulae [455d639]
- 🐛 fix a bug [effedb1]
    * 🐛 Fix bug 01 (90baf51)
- ✏️ update version to match with SemVer specifications [8163b9e]
- 🐛 fix a bug in unix script generation [6874eee]
- 🐛 fix and improve regex [9933554]
- 🐛 fixed a bug affecting the &#x27;slash&#x27; character when generating output paths [d83f07e]
- 🐛 correction of a typo creating a bug [945daa9]
    * 🐛 correction of a typo creating a bug (6f1667c)
- 🐛 fix fixed path issue [f1a1a7d]
- 🐛 fix a little bug where the computername was not in the filename (pwsh script) and make an archive [744515f]
- 🐛 fix a bug when a space is present in the path [ee9e186]
- 🐛 fix path error on macOS [e4e583c]
- 🐛 fix: config file not created if directory exists [960c725]
- 🐛 fix: fix xml generation for python 3.10 [2c4ab0d]
- 🐛 Fixed a bug where only the last category was taken into account when generating collection scripts [ca1a15d]
- ✏️ Change output extension for homogenizing purposes [9b46c49]
- ✏️ adjustment of the import order in accordance with PEP 8 [ee66b32]
- 🐛 Fix check runner with DeepL ignore tag on category name [292825d]
- ✏️ Suppression of ignore_tags in report generation [55cbdf3]
- ✏️ Fix typos [e4875f5]
    * ✏️ Fix typo (9661ab5)
    * ✏️ Fix typo (aa450be)
    * ✏️ Fix typo (d86590c)
    * ✏️ Fix typos (b3000ff)
- 🐛 Handling of an exception identified when using the use case &#x27;audit&#x27; on a French Windows system [594cb52]
- 🐛 Fixed a bug affecting .po files when generating reports [1195239]
- 🐛 Fixed a bug occuring on windows when running commands [2b4e0d3]
- 🐛 Fixed a side effect following the merge request [7a00f8e]
- 🐛 Regex, if you love it, you don&#x27;t count ... [8e3be16]
- 🐛 Fixed regex... [2480f14]
- 🐛 Fixed a bug that did not take the arguments in the collection command into account and added some improvements [1584f39]
- 🐛 Removal of redundant debugging calls [157885c]
- ✏️ Changing the output file extension [56f6020]
- 🐛 Fix low impact bug [abf87ea]
- ✏️ Sort modules [d116c28]

### Security

- 🔒 fix security issue by updating requirements [0d71517]
- 🔒 Creating a Security policy [a78e699]

### Miscellaneous

- 📝 update documentation [9f6d851]
    * 📝 update documentation (e71e5fd)
    * 📝 update documentation (71edeff)
- 📦 update submodules [db81907]
    * ⬆️ upgrade submodules (1f043f7)
    * 📦 update submodules (6e20412)
    * 📦 update submodules (cda6090)
    * 🍱 update submodules (5656bb9)
    * 🍱 update submodules (4c85ee1)
    * 🔧 update submodule (5aee41e)
    * 🔧 update submodules list (eaeb505)
- 📝 add CONTRIBUTING [1d030c5]
- 📝 update README [b5a6246]
    * 📝 update README (18fa936)
    * 📝 update README (a0d02ac)
    * 📝 update README (267f076)
    * 📝 update README (75377d8)
    * 📝 update README (adc8a2d)
    * 📝 update README (4317327)
    * 📝 update README (e81cb7f)
    * 📝 update README (1072013)
    * 📝 update README (d412682)
    * 📝 update README (4c2108c)
    * 📝 update README (18c40eb)
    * 📝 update README (97fa770)
    * 📝 update README (99b0ae7)
    * 📝 update README (57c7b47)
    * 📝 update README (ebd22c2)
    * 📝 update README (69f6b80)
    * 📝 Update README.md (3c59672)
    * 📝 Update README.md (1cb84e4)
    * 📝 Update README.md (e73756f)
    * 📝 Update README.md (d37af47)
    * 📝 Update README.md (eb66149)
    * 📝 Update README.md (a1559e0)
    * 📝 Update README (cdac9b7)
- 📝 add troubleshooting section [b989afc]
-  Merge remote-tracking branch &#x27;origin/main&#x27; into main [01b19cc]
-  Updated submodule baselines [57b27c3]
    *  Updated submodule baselines (f227ed4)
- 📄 update copyright info [32b519c]
    * 📄 update copyright info (8caf06e)
-  Updated submodule octoconf/interface_adapters/octowriter [eab8b7b]
    *  Updated submodule octoconf/interface_adapters/octowriter (c865166)
- 📝 update CHANGELOG [a2c3336]
- 🧑‍💻 add issue templates [13453eb]
    * 🧑‍💻 add issue templates (acc2b5c)
-  Create .gitlab-ci.yml file [b202563]
- 📦 update gitmodules file [aa15a19]
- 📄 update copyrights among other stuff [cd7034c]
- 🚧 push diff - unit test failed [d098968]
- 📦 update dependency [a1542d3]
- 🚧 working on report generation to generate csv, pdf and html reports [b6e5366]
- 🚧 add encryption wrapper [6afcf13]
- 📝 update description [378c2f1]
-  :fix: fix a path error [6e3bc94]
-  :fix: fix the version comparison operation [bb30072]
- 📝 changing configuration levels [5fb37f8]
- ⚗️ experimentation with the function of preprocess_collection_cmd and correction of a bug [62bd936]
- ⚰️ remove dead code [4912d20]
- 📝 update documentation to add level notion [cc022ca]
- 🙈 update .gitignore file [d42c819]
    * 🙈 update .gitignore file (3b1bc10)
- 🧪 apply the previous modifications to the unit tests [2addbc2]
- 📝 docs: update readme file [6e788e2]
    * 📝 docs: update readme file (4e8d267)
    * 📝 docs: update readme file (93f9621)
    * 📝 docs: update readme file (f13968c)
    * 📝 docs: update readme file (0ea513e)
    * 📝 docs: update readme (4e3f366)
    * 📝 docs: update readme file (c9cbc13)
- 🧪 test: add python 3.10 tests [7b5332d]
- 🧪 test: fixing some tests [25d15ff]
- 🧪 test: edit github action workflow [de91c7f]
- 📝 docs: update basic information [64d798e]
-  Merge branch &#x27;main&#x27; of github.com:Nillyr/octoconf [bf0e085]
-  Signed-off-by: Nicolas GRELLETY &lt;ngy.cs@protonmail.com&gt; [d257b70]
- 🌐 style: definition of the default value in case of non specification [2bc2660]
- 📦 Update Makefile rules [5d635c6]
    * 📦 Update Makefile rules (30ee606)
    * 📦 Updated Makefile (f978db8)
- 🌐 Explicit addition of the output locale when running commands on unix/linux [ba6c2ae]
- 🙈 Update .gitignore file [98c348a]
    * 🙈 Updated gitignore (f8cdb51)
    * 🙈 Update .gitignore file (4d578a3)
- 📝 Update documentation [4315762]
    * 📝 Update documentation (c32b5be)
    * 📝 Update user documentation (28f2f68)
    * 📝 Update user documentation (8eae948)
    * 📝 Update user documentation (6c7c5cd)
    * 📝 Updating documentation (861d335)
- 🧑‍💻 Improved regular expression when creating folders eliminating special characters [e9f8c1d]
- 🛂 Running scripts as root is not a good idea [f773a16]
- 🏷️ Adding reference for checks [acbda9c]
- 📦 Update setup.py to include yaml checklists [a75dd09]
- 💡 Add comments in source code [2b653c5]
- 💡 Update comments in source code [f14ece3]
- 🤡 Making small adjustments [b8d45a1]
- 📝 Documentation of the translation feature [df4242e]
- 📝 Update submodule [8f81b8f]
    * 📦 Updated submodule (3635451)
    * ⬆️ Updated submodule (f0ca2f0)
    * 📦 Updated submodule (789eb0d)
    * ⬆️ Upgrade submodule (c433c25)
-  Merge pull request #7 from Nillyr/yaml-checklist-parser [b1b2056]
    *  Merge pull request #6 from Nillyr/checklist (4ea233e)
- 📝 Update .gitmodules [d2b85e3]
- 📝 Version update [40b8f35]
    * 🚀 Version upgrade (f0371f1)
    * 📦 Version upgrade (868fb63)
    * 📦 Version upgrade (a89ca82)
- 🩹 Fix range when generating charts [dbecabd]
- 📝 Update version [d0cc31e]
    * 📦 Update version (e150eb2)
    * 📝 Update version (ebf06ac)
    * 📝 Update version (558449c)
- 🚧 Implementation of the use case allowing the translation of checklists [246a491]
- ⚰️ Removed dead code [df9e247]
    * ⚰️ Removed dead code (8851882)
- 📝 Updated some information [9f9b7d2]
- 🩹 Added the submodule at compile time and updated the links in the documentation [652c66d]
    * 🩹 Added the submodule at compile time and updated the links in the documentation (dd2dc20)
- 📝 Updated docs [aaecf31]
- 📝 Update developer documentation [fcb1a8f]
    * 📝 Update developer documentation (b553fa8)
- 📝 Added user documentation [86fece9]
- 🚧 Preparation of the release candidate [3f6d81e]
-  Merge pull request #4 from Nillyr/3_integrated_checklists [a5cb264]
- 📝 Update feature_request [e304d24]
- 📝 Create feature_request issue template [f77b1c1]
- 📝 Updated README.md [f0076bf]
    * 📝 Updated README.md (f9d28d2)
    * 📝 Updated README.md (bb49300)
- 📄 Added copyright information [aeea9cf]
- 📄 Updated license [938b0a8]
-  Merge pull request #2 from Nillyr/fix-issue-01 [79194f2]
- 📦 Update of checklists [7f2c3a1]
- 📝 Update issue templates [e8803ec]
- 🔨 Added a helper script to run the tests and generate the report [1375a05]
- 📝 Added the coverage percentage of the code by using &#x27;coverage report -m&#x27; [e3458d5]
- 🗑️ Removed the internationalization option for the collection script generation [e1961b1]
- 📝 Update Readme.md file [0e8b49b]
    * 📝 Update Readme.md file (3505b1a)
    * 📝 Update Readme.md file (3e53b5b)
- 🌐 Addition of internationalization [33ca1e2]
- 💡 Adding docstrings (PEP 257) [e967727]
- 🚧 Implementation of PEP 8 compliance [3fa1669]
- 📝 Update build file [6ae20ac]
- 🚧 Adding automatic report generation feature [ae4b2c9]
- 🚧 Preparing the use case analyze [fdb61d4]
- 🩹 A non performable check may have a collection command. For instance, gather all installed KB but not able to compare with the lastest deploy KB. [1a0748b]
- 💩 Renaming a method that does not do what it says it does in its name [5baf40c]
- 📦 Create an egg file [5dbf98d]
- 🩹 Retrieval of collection commands and not checks [8b93015]
- 🚧 Add windows platform decorators [d6f52a6]
- 🚧 Add macOS platform decorator [3b74786]
- 🚧 Work on the use case of generating a collection script [208c0bb]
- 📝 Update README file [1f4037a]
    * 📝 Update README file (7a838fd)
    * 📝 Update README file (7159722)
    * 📝 Update README file (3c588e8)
    * 📝 Update README file (530b39a)
    * 📝 Update README file (efc613b)
    * 📝 Update README file (22f84d6)
    * 📝 Update README file (efbc822)
    * 📝 Updating README (726b98b)
- 📝 Update the template accordingly [058f2e8]
- 🏷️ Defining models [82c088e]
- 🤡 Defining usage and adding cool stuff [d562030]
-  pushpin: Update of the minimum version of python3 required [58dd887]
    * 📌 Update of the minimum version of python3 required (4f7882f)
- 📝 Update README and requirements [f81b24c]
-  Initial commit [47f0252]


