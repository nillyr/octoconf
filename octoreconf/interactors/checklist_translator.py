# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import sys

from icecream import ic
import inject

from octoreconf.ports import IChecklist, ITranslator


class ChecklistTranslatorInteractor:
    """
    Use case for the translation of checklists.
    """

    @inject.autoparams("checklist", "translator")
    def __init__(self, checklist: IChecklist, translator: ITranslator) -> None:
        self._checklist = checklist
        self._translator = translator

    def _translate(self, text, source_lang, target_lang) -> str:
        return self._translator.translate(text, source_lang, target_lang)

    def execute(self, args) -> int:
        checklist, output, source_lang, target_lang = ic(args.values())
        source_lang = source_lang.upper()
        target_lang = target_lang.upper()

        self._checklist.parse_checklist(checklist)
        categories = []
        categories.append({"categories": self._checklist.get_categories()})
        try:
            for category in categories[0]["categories"]:
                category.name = self._translate(category.name, source_lang, target_lang)
                for checkpoint in category.checkpoints:
                    checkpoint.title = self._translate(
                        checkpoint.title, source_lang, target_lang
                    )
                    checkpoint.description = self._translate(
                        checkpoint.description, source_lang, target_lang
                    )
                    for check in checkpoint.checks:
                        check.title = self._translate(
                            check.title, source_lang, target_lang
                        )
                        try:
                            check.description = self._translate(
                                check.description, source_lang, target_lang
                            )
                        except:
                            pass
                        check.recommandation_on_failed = self._translate(
                            check.recommandation_on_failed, source_lang, target_lang
                        )

            with open(output, "w") as output_file:
                output_file.write(self._checklist.get_original_format(categories))
            return 0
        except Exception as _err:
            print(f"{self.__class__} error: {_err}", file=sys.stderr)
            return 1
