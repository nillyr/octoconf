# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import logging

import requests

from . import config as deepl_config
from .exceptions import DeepLError
from octoconf.interfaces.translator import ITranslator
import octoconf.utils.config as config
from octoconf.utils.logger import *

logger = logging.getLogger(__name__)


class DeepL(ITranslator):
    """
    Simplistic implementation to translate baselines using the DeepL translator.
    """

    def __init__(self) -> None:
        self._url = "/".join(
            [
                config.get_config("translator", "deepl_api_base")
                if config.get_config("translator", "deepl_api_base") != ""
                else deepl_config.const.BASE_URL,
                config.get_config("translator", "deepl_api_version")
                if config.get_config("translator", "deepl_api_version") != ""
                else deepl_config.const.API_VERSION,
                config.get_config("translator", "deepl_api_endpoint")
                if config.get_config("translator", "deepl_api_endpoint") != ""
                else deepl_config.const.ENDPOINT,
            ]
        )

    def translate(self, text, source_lang, target_lang) -> str:
        """
        Method to send a request to the deepl API.

        Use of the ignore tag to avoid translating some parts of the baseline (especially the executed commands).
        """

        api_key = config.get_config("translator", "deepl_api_key")
        if any([api_key == "", api_key == "TO_BE_DEFINED"]):
            raise DeepLError(
                403, "'deepl_api_key' must be set before using the feature"
            )

        if source_lang not in deepl_config.const.SUPPORTED_LANG.keys():
            raise DeepLError(400, "Value for 'source_lang' not supported.")
        if target_lang not in deepl_config.const.SUPPORTED_LANG.keys():
            raise DeepLError(400, "Value for 'target_lang' not supported.")

        data = {
            "auth_key": api_key,
            "text": text if text else "",
            "source_lang": source_lang,
            "target_lang": target_lang,
            "tag_handling": "xml",
            "ignore_tags": "x",
        }

        try:
            response = requests.post(self._url, data=data)
        except Exception as _err:
            logger.exception(f"Unmanaged Error: {_err}")
            return ""
        
        if response.status_code != 200:
            raise DeepLError(response.status_code, response.json()["message"])

        res = response.json()
        if not res:
            return ""

        return res["translations"][0]["text"]
