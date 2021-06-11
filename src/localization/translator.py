import json
import inspect

from localization import vocabularies
from custom_logging import logger


# Сделать класс с методами
class Translator:
    # def __init__(self):
    #     pass
        # self.loc = loc
        # self.data = data
        # source_name = inspect.stack()[1].function   # or [1][3]
        # logger.debug(f"source_name - {source_name}")
        # method_name = "trl_" + source_name
        # self.vocabulary = getattr(vocabularies, source_name.upper())[loc]  # will need to handle the exception
        # logger.debug(f"vocabulary - {self.vocabulary}")

    # def exec(self, method_name):
    #     return getattr(Translator, method_name)(self.loc, self.data, self.vocabulary)

    @staticmethod
    def trl_weather_data(loc: str, data: dict):
        vocabulary = vocabularies.WEATHER_DATA[loc]
        translated_data = {}
        for key in data.keys():
            if key in vocabulary:
                translated_data[vocabulary[key]] = data.get(key)
        return json.dumps(translated_data, indent=2, ensure_ascii=False)

    @staticmethod
    def welcome_back(loc: str, data: str):
        vocabulary = vocabularies.WELCOME_BACK[loc]
        translated_data = f"{vocabulary} {data}!"
        return translated_data


def translator(loc: str, data: dict, *args) -> str:
    source_name = inspect.stack()[1].function
    logger.debug(f"source_name - {source_name}")

    vocabulary = getattr(vocabularies, source_name.upper())[loc]    # will need to handle the exception
    logger.debug(f"vocabulary - {vocabulary}")

    translated_data = {}
    for key in data.keys():
        logger.debug(f"key - {key}")
        if key in vocabulary:
            # logger.debug(f"vocabulary[key] - {vocabulary[key]}")
            translated_data[vocabulary[key]] = data.get(key)
            # logger.debug(f"translated_data.items() - {translated_data.items()}")

    return json.dumps(translated_data, indent=2, ensure_ascii=False)


# obj_format_dict = {
#         "Заболело": obj_format.confirmed,
#         "Выздоровело": obj_format.recovered,
#         "Умерло": obj_format.deaths,
#         "Локация": obj_format.location,
#     }
#     obj_json = json.dumps(obj_format_dict, indent=2, ensure_ascii=False)
#
#     for r in (("Global", "Весь мир"), ("Belarus", "Беларусь"), ("Russia", "Россия"), ("US", "США")):
#         obj_json = obj_json.replace(*r)
