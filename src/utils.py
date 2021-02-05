from get_data.get_data_c19 import get_cv19_data


def choice_of_answer(ar):
    check1 = ["hi", "hello", "good morning", "good afternoon", "good evening", "привет", "здравствуй", "здравствуйте",
              "доброе утро", "добрый день", "добрый вечер"]
    check2 = ["дай ответ на главный вопрос жизни, вселенной и вообще",
              "give an answer to the ultimate question of life, the universe, and everything"]
    if ar.lower() in check1:
        # print(ar)
        return ar
    elif ar.lower() in check2:
        # print("42")
        return "42"
    # print("ok")
    else:
        return "Ok"


def select_event_w_entities(arg):
    switcher = {
        "/covid19global": lambda: get_cv19_data(),
        "/covid19blr": lambda: get_cv19_data("Belarus"),
        "/covid19rus": lambda: get_cv19_data("Russia"),
        "/covid19usa": lambda: get_cv19_data("US"),
    }

    # return switcher.get(arg, "Ok")
    return switcher[arg]()
