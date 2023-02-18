# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from pathlib import Path
import sys

from icecream import ic
import inject

from octoconf.components.translators import TranslatorCache
from octoconf.interfaces import IBaseline, ITranslator

from octoconf.entities import *

class BaselineTranslatorUseCase:
    """
    Use case for the translation of baselines.
    """

    _cache: TranslatorCache

    @inject.autoparams("baseline_adapter", "translator")
    def __init__(self, baseline_adapter: IBaseline,
                translator: ITranslator) -> None:
        self._baseline_adapter = baseline_adapter
        self._translator = translator
        self._cache = TranslatorCache()

    def _translate(self, text, source_lang, target_lang) -> str:
        cached_translation = self._cache.retrieve_from_cache(text)
        if cached_translation is not None:
            return cached_translation

        translated = ""
        try:
            translated = self._translator.translate(
                                                text,
                                                source_lang,
                                                target_lang)
            self._cache.populate_cache(text, translated)
        except Exception as _err:
            print(f"{self.__class__} error: {_err}", file=sys.stderr)
        finally:
            return translated

    @TranslatorCache.decorator
    def execute(self, args) -> int:
        baseline_file_path, output_directory, source_lang, target_lang = ic(args.values())

        if Path(output_directory).is_dir():
            user_risk_acceptance = False
            try:
                while(not user_risk_acceptance):
                    confirmation = input(f"[!] The directory '{output_directory}' already exists. By using this directory, you may lose data.\n[!] Do you REALY want to continue? (y/N): ")
                    if confirmation == "" or confirmation.upper() == "N":
                        return 1
                    elif confirmation.upper() == "Y":
                        user_risk_acceptance = True
            except:
                return 1
        baseline = self._baseline_adapter.load_baseline_from_file(Path(baseline_file_path))

        baseline.title = self._translate(
                                    ic(baseline.title),
                                    source_lang,
                                    target_lang)

        for category in baseline.categories:
            category.category = self._translate(
                                            ic(category.category),
                                            source_lang,
                                            target_lang)
            category.name = self._translate(
                                        ic(category.name),
                                        source_lang,
                                        target_lang)
            category.description = self._translate(
                                            ic(category.description),
                                            source_lang,
                                            target_lang)

            for rule in category.rules:
                rule.title = self._translate(
                                            ic(rule.title),
                                            source_lang,
                                            target_lang)
                rule.description = self._translate(
                                            ic(rule.description),
                                            source_lang,
                                            target_lang)
                rule.recommendation = self._translate(
                                            ic(rule.recommendation),
                                            source_lang,
                                            target_lang)

        return self._baseline_adapter.save_translated_baseline(
            Path(baseline_file_path),
            ic(baseline),
            Path(output_directory))
