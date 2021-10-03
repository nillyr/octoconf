from abc import ABCMeta, abstractstaticmethod


class ILanguageFactory(metaclass=ABCMeta):
    @abstractstaticmethod
    def get_language(language_name, platform):
        pass
