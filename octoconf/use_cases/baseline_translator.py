# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging
from pathlib import Path

import inject

from octoconf.components.translators.cache import TranslatorCache
from octoconf.interfaces.baseline import IBaseline
from octoconf.interfaces.translator import ITranslator
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class BaselineTranslatorUseCase:
    """
    Use case for the translation of baselines.
    """

    _cache: TranslatorCache

    @inject.autoparams("baseline_adapter", "translator")
    def __init__(self, baseline_adapter: IBaseline, translator: ITranslator) -> None:
        self._baseline_adapter = baseline_adapter
        self._translator = translator
        self._cache = TranslatorCache()

    def _translate(self, text, source_lang, target_lang) -> str:
        logger.debug(f"Looking for '{text}' in cache")
        cached_translation = self._cache.retrieve_from_cache(text)
        if cached_translation is not None:
            return cached_translation

        translated = ""
        try:
            translated = self._translator.translate(text, source_lang, target_lang)
            self._cache.populate_cache(text, translated)
            return translated
        except Exception as _err:
            logger.exception(f"Catch an exception: {_err}")
            raise _err

    @TranslatorCache.decorator
    def execute(self, args) -> int:
        logger.info(f"Running baseline translation use case")
        baseline_file_path, output_directory, source_lang, target_lang = args.values()
        logger.debug(
            f"Using the following args: baseline_file_path = {baseline_file_path}, output_directory = {output_directory}, source_lang = {source_lang}, target_lang = {target_lang}"
        )

        if Path(output_directory).is_dir():
            user_risk_acceptance = False
            try:
                while not user_risk_acceptance:
                    confirmation = input(
                        f"[!] The directory '{output_directory}' already exists. By using this directory, you may lose data.\n[!] Do you REALY want to continue? (y/N): "
                    )
                    if confirmation == "" or confirmation.upper() == "N":
                        return 1
                    elif confirmation.upper() == "Y":
                        user_risk_acceptance = True
            except:
                logger.exception("User risk acceptance finished with an error")
                return 1

        baseline = self._baseline_adapter.load_baseline_from_file(
            Path(baseline_file_path)
        )
        try:
            baseline.title = self._translate(baseline.title, source_lang, target_lang)

            for category in baseline.categories:
                category.category = self._translate(
                    category.category, source_lang, target_lang
                )
                category.name = self._translate(category.name, source_lang, target_lang)
                category.description = self._translate(
                    category.description, source_lang, target_lang
                )

                for rule in category.rules:
                    rule.title = self._translate(rule.title, source_lang, target_lang)
                    rule.description = self._translate(
                        rule.description, source_lang, target_lang
                    )
                    rule.recommendation = self._translate(
                        rule.recommendation, source_lang, target_lang
                    )

            return self._baseline_adapter.save_translated_baseline(
                Path(baseline_file_path), baseline, Path(output_directory)
            )
        except Exception as _err:
            logger.exception(f"Catch an exception: {_err}")
            return 1
