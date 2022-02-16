# @copyright Copyright (c) 2021-2022 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

from icecream import ic
import inject

from octoconf.components.translators import TranslatorCache
from octoconf.ports import IChecklist, ITranslator


class ChecklistTranslatorInteractor:
    """
    Use case for the translation of checklists.
    """

    _cache: TranslatorCache

    @inject.autoparams("checklist", "translator")
    def __init__(self, checklist: IChecklist, translator: ITranslator) -> None:
        self._checklist = checklist
        self._translator = translator
        self._cache = TranslatorCache()

    def _translate(self, text, source_lang, target_lang) -> str:
        cached_translation = self._cache.retrieve_from_cache(text)
        if cached_translation is not None:
            return cached_translation

        translated = self._translator.translate(text, source_lang, target_lang)
        self._cache.populate_cache(text, translated)
        return translated

    @TranslatorCache.decorator
    def execute(self, args) -> None:
        checklist, output, source_lang, target_lang = ic(args.values())

        self._checklist.parse_checklist(checklist)
        categories = []
        categories.append({"categories": self._checklist.get_categories()})
        try:
            categories = categories[0]["categories"]
            for category in categories:
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
                        check.recommendation_on_failed = self._translate(
                            check.recommendation_on_failed, source_lang, target_lang
                        )

            with open(output, "w") as output_file:
                print(f"[*] Writing translated checklist in '{output}'")
                output_file.write(self._checklist.get_original_format(categories))
        except Exception as _err:
            print(f"{self.__class__} error: {_err}", file=sys.stderr)
