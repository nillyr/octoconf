# @copyright Copyright (c) 2021-2023 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://github.com/nillyr/octoconf
# @since 1.0.0b

from pathlib import Path
import sys

import polib


class Locale:
    """
    Class responsible for retrieving the internationalization files in order to return the text in the language defined by the user.
    It takes as argument the ISO 639-1 code. See also: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    """

    _basedir = Path(__file__).resolve().parent

    def __init__(self, lang: str = "EN"):
        self._dict = dict()
        self._locale = lang.upper()
        self._pofilename = f"{lang.lower()}_{lang.upper()}.po"
        self._parse_po_file()

    def _parse_po_file(self):
        """
        Parse the ".po" file of the language chosen by the user and populate the dictionary.
        """
        path = str(self._basedir / self._pofilename)
        try:
            pofile = polib.pofile(path, encoding="utf-8")
            for entry in pofile:
                self._dict[entry.msgid] = entry.msgstr
        except IOError as _err:
            print(
                f"Error: file not found or syntax error. {_err} file = {str(path)}",
                file=sys.stderr,
            )

    def gettext(self, msgid):
        """
        Returns the text in the language defined by the user given the key provided.
        """
        try:
            return self._dict[msgid]
        except KeyError as _err:
            print(
                f"Error: key {_err} not found in class {__class__.__name__}.",
                file=sys.stderr,
            )

    def get_locale(self) -> str:
        return self._locale
