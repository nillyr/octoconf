# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

from abc import ABC, abstractmethod


class ITranslator(ABC):
    @abstractmethod
    def translate(self, text, source_lang, target_lang) -> str:
        """
        Translate a text from a source language to a target language.
        """
        pass
