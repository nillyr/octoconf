# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/Nillyr/octoreconf
# @since 1.0.0b

import sys

from icecream import ic
import inject

from octoreconf.components.translators.translator import ITranslator


class ChecklistTranslatorInteractor:
    """
    Use case for the translation of checklists.
    """

    @inject.autoparams("translator")
    def __init__(self, translator: ITranslator) -> None:
        self._translator = translator

    def execute(self, args) -> int:
        checklist, output, source_lang, target_lang = ic(args.values())

        try:
            text = self._translator.translate(
                "Work in Progress", source_lang.upper(), target_lang.upper()
            )
            print(text)
            return 0
        except Exception as _err:
            print(f"{self.__class__} error: {_err}", file=sys.stderr)
            return 1
