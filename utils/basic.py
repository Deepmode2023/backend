

def contains_instace(list_contains: list[str], compare_str: str) -> bool:
    return any(compare_str in item for item in list_contains)


def contains_with_list(list_contains: list[str], compare_list: list[str]) -> bool:
    compare_condition = 0
    for compare_item in compare_list:
        compare_condition += contains_instace(
            list_contains=list_contains, compare_str=compare_item)

    return True if compare_condition > 0 else False


def build_kwargs_not_none(**kwargs):
    return {key: value for key, value in kwargs.items() if value != None and value != ''}
