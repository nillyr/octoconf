# @copyright Copyright (c) 2021 Nicolas GRELLETY
# @license https://opensource.org/licenses/GPL-3.0 GNU GPLv3
# @link https://gitlab.internal.lan/octo-project/octoconf
# @link https://github.com/nillyr/octoconf
# @since 0.1.0

import json
from pathlib import Path


class TranslatorCache:
    """
    Cache translated text to avoid useless requests.
    Because it's a simplistic use case, the dictionary approach has been choosed.
    """

    _instance = None
    _cache: dict = dict()
    _cache_directory: str = ".cache"
    _cache_filename: str = ""

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_cache(self, source_lang: str, target_lang: str) -> None:
        path = Path.home() / ".cache" / "octoconf"
        path.mkdir(parents=True, exist_ok=True)

        self._cache_filename = str(path / f"{source_lang}-{target_lang}.json")
        with open(self._cache_filename, "w+") as cache_file:
            try:
                self._cache = json.load(cache_file)
            except:
                pass

    def write_cache_to_disk(self) -> None:
        with open(self._cache_filename, "w+") as cache_file:
            json.dump(self._cache, cache_file)

    def populate_cache(self, key: str, value: str) -> None:
        if key not in self._cache.keys():
            self._cache[key] = value

    def retrieve_from_cache(self, key: str) -> str:
        if key in self._cache.keys():
            return self._cache[key]

    def decorator(func):
        def inner(*args, **kwargs):
            args[1]["source_lang"] = args[1]["source_lang"].upper()
            args[1]["target_lang"] = args[1]["target_lang"].upper()
            TranslatorCache().load_cache(args[1]["source_lang"], args[1]["target_lang"])
            func(*args, **kwargs)
            TranslatorCache().write_cache_to_disk()

        return inner
