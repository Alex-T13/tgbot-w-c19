import inspect
import json

from localization import vocabularies
from custom_logging import logger


class Translator:
    @staticmethod
    def data_translation(loc: str, data: dict) -> str:
        source_name = inspect.stack()[1].function  # or [1][3]
        ensure_ascii = True if loc == 'en' else False
        try:
            vocabulary = getattr(vocabularies, source_name.upper())[loc]
            if not vocabulary:
                raise AttributeError
        except AttributeError:
            logger.debug('Err: Dictionary not found - data not translated!')
            return json.dumps(data, indent=2, ensure_ascii=ensure_ascii)
        else:
            translated_data = {}
            for key in data.keys():
                if key in vocabulary:
                    translated_data[vocabulary[key]] = data.get(key)
            return json.dumps(translated_data, indent=2, ensure_ascii=ensure_ascii)

    @staticmethod
    def trl_welcome_back(loc: str, data: str):
        vocabulary = vocabularies.WELCOME_BACK[loc]
        translated_data = f"{vocabulary} {data}!"
        return translated_data

    @staticmethod
    def trl_choice_of_answer(loc: str, data: str):
        vocabulary = vocabularies.CHOICE_OF_ANSWER[loc]
        translated_data = f"{data}, {vocabulary}"
        return translated_data
