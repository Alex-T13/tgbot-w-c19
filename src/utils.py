from get_data.get_data_c19 import get_cv19_data


def select_event(ar: str):
    switcher = ["hi", "hello", "good morning", "good afternoon", "good evening",
                "привет", "здравствуй", "здравствуйте", "доброе утро",
                "добрый день", "добрый вечер"
                ]
    if ar.lower() in switcher:
        return ar
    if ar.lower() == "дай ответ на главный вопрос жизни, вселенной и вообще" or \
            "give an answer to the ultimate question of life, the universe, and everything":
        return "42"
    return "Ok"


def select_event_w_entities(arg: str):
    switcher = {
        "/covid19global": lambda: get_cv19_data(),
        "/covid19blr": lambda: get_cv19_data("Belarus"),
        "/covid19rus": lambda: get_cv19_data("Russia"),
        "/covid19usa": lambda: get_cv19_data("US"),
    }

    # return switcher.get(arg, "Ok")
    return switcher[arg]()


# get_cv19_data(event_selection("/covid19-usa"))
# select_event_w_entities("/covid19rus")

