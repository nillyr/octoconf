# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

import os

from dotenv import load_dotenv

from octoconf.utils import const

load_dotenv()
const.API_KEY = os.getenv("DEEPL_API_KEY")

const.BASE_URL = "https://api-free.deepl.com"
const.API_VERSION = "v2"
const.ENDPOINT = "translate"

const.SUPPORTED_LANG = {
    "BG": "Bulgarian",
    "CS": "Czech",
    "DA": "Danish",
    "DE": "German",
    "EL": "Greek",
    "EN-GB": "English (British)",
    "EN-US": "English (American)",
    "EN": "English (unspecified variant for backward compatibility; please select EN-GB or EN-US instead)",
    "ES": "Spanish",
    "ET": "Estonian",
    "FI": "Finnish",
    "FR": "French",
    "HU": "Hungarian",
    "IT": "Italian",
    "JA": "Japanese",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "NL": "Dutch",
    "PL": "Polish",
    "PT-PT": "Portuguese (all Portuguese varieties excluding Brazilian Portuguese)",
    "PT-BR": "Portuguese (Brazilian)",
    "PT": "Portuguese",
    "RO": "Romanian",
    "RU": "Russian",
    "SK": "Slovak",
    "SL": "Slovenian",
    "SV": "Swedish",
    "ZH": "Chinese",
}
