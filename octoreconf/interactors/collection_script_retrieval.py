from icecream import ic
import inject

from octoreconf.ports import IChecklist
from octoreconf.ports.script_generator.language_abstract_factory import ILanguageFactory


class CollectionScriptRetrievalInteractor:
    """
    Use case for creating, from a checklist, a script to collect the configuration of the system (or the application) to be audited.
    """

    _newline = lambda _, x: "\n" if x in ("linux", "mac") else "\r\n"

    @inject.autoparams("checklist", "factory")
    def __init__(self, checklist: IChecklist, factory: ILanguageFactory) -> None:
        self._checklist = checklist
        self._factory = factory

    def execute(self, args):
        checklist, output, language, platform = ic(args.values())

        self._checklist.parse_checklist(checklist)
        commands = self._checklist.get_commands()
        script = self._factory.get_language(platform, language)

        with open(output, "w", newline=self._newline(platform)) as file:
            content = script.write_script(commands, script.write_checks_cmds)
            [file.write(x) for x in content]
