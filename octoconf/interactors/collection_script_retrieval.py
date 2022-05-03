# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from icecream import ic
import inject

from octoconf.ports import IChecklist
from octoconf.ports.script_generator.language_abstract_factory import ILanguageFactory


class CollectionScriptRetrievalInteractor:
    """
    Use case for creating, from a checklist, a script to collect the configuration of the system (or the application) to be audited.
    """

    _newline = lambda _, x: "\n" if x in ("gnu/linux", "linux", "mac") else "\r\n"

    @inject.autoparams("checklist", "factory")
    def __init__(self, checklist: IChecklist, factory: ILanguageFactory) -> None:
        self._checklist = checklist
        self._factory = factory

    def execute(self, args):
        checklist, output, platform = ic(args.values())

        self._checklist.parse_checklist(checklist)
        commands = self._checklist.get_commands()
        script = self._factory.get_language(platform)

        with open(output, "w", newline=self._newline(platform)) as file:
            content = script.write_script(commands, script.write_checks_cmds)
            [file.write(x) for x in content]
