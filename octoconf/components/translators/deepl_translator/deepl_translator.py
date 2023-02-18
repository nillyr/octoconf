# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import sys

import requests

from . import config
from .exceptions import DeepLError
from octoconf.interfaces import ITranslator


class DeepL(ITranslator):
    """
    Simplistic implementation to translate baselines using the DeepL translator.
    """

    def __init__(self) -> None:
        self._url = "/".join(
            [config.const.BASE_URL, config.const.API_VERSION, config.const.ENDPOINT]
        )

    def translate(self, text, source_lang, target_lang):
        """
        Method to send a request to the deepl API.

        Use of the ignore tag to avoid translating some parts of the baseline (especially the executed commands).
        """
        if source_lang not in config.const.SUPPORTED_LANG.keys():
            raise DeepLError(400, "Value for 'source_lang' not supported.")
        if target_lang not in config.const.SUPPORTED_LANG.keys():
            raise DeepLError(400, "Value for 'target_lang' not supported.")

        data = {
            "auth_key": config.const.API_KEY,
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "tag_handling": "xml",
            "ignore_tags": "x",
        }
        try:
            response = requests.post(self._url, data=data)
        except Exception as _err:
            print(f"Unmanaged Error: {_err}", file=sys.stderr)
        if response.status_code != 200:
            raise DeepLError(response.status_code, response.json()["message"])

        res = response.json()
        if not res:
            return None

        return res["translations"][0]["text"]
