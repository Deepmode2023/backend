
def extract_key_or_value(from_dict_exclude: dict, exclude_key_list: list):
    def is_contains(key, value):
        return exclude_key_list.__contains__(key) or exclude_key_list.__contains__(value)

    return {key: from_dict_exclude[key] for key in from_dict_exclude if not is_contains(key, from_dict_exclude[key])}
