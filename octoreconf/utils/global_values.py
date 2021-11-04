from octoreconf.utils import Locale


def set_localize(lang: str):
    global localize
    localize = Locale(lang)
