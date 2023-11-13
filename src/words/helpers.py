
from utils.basic import build_kwargs_not_none


def return_words_kwarg_after_check_permission(is_admin: bool, access_field_not_admin: list[str], **kwargs):
    exist_kwargs = build_kwargs_not_none(**kwargs)
    if not is_admin:
        return {key: exist_kwargs.get(key) for key in access_field_not_admin if exist_kwargs.get(key)}

    return exist_kwargs
