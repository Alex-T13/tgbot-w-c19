from get_data.get_data_c19 import get_cv19_data


def event_selection(arg):  # session: ClientSession
    switcher = {
        "/covid19-global": lambda: get_cv19_data(),
        "/covid19-blr": lambda: get_cv19_data("Belarus"),
        "/covid19-rus": lambda: get_cv19_data("Russia"),
        "/covid19-usa": lambda: get_cv19_data("US"),
    }

    # return switcher.get(arg, "Ok")
    return switcher[arg]()


# get_cv19_data(event_selection("/covid19-usa"))
event_selection("/covid19-rus")