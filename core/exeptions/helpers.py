from . import ExeptionsSchema as exeptions
from fastapi import status
from core.schema.schemas import TReturnedModel
from pydantic import ValidationError
from functools import wraps


def exeption_handling_decorator(f):
    @wraps(f)
    async def wrapper(**kwargs):
        try:
            return await f(**kwargs)

        # BASIC EXEPTIONS
        except exeptions.DoNotUpdateFieldsInDB:
            return TReturnedModel(details=exeptions.DoNotUpdateFieldsInDB().get_message,
                                  status=status.HTTP_404_NOT_FOUND, data=None)

        except exeptions.NoValidTokenRaw:
            return TReturnedModel(details=exeptions.NoValidTokenRaw().get_message,
                                  status=status.HTTP_400_BAD_REQUEST, data=None)

        except exeptions.YouDontHaveAccessExeptions:
            return TReturnedModel(details=exeptions.YouDontHaveAccessExeptions().get_message,
                                  status=status.HTTP_401_UNAUTHORIZED, data=None)

        except exeptions.DontExistItemInsideDB:
            return TReturnedModel(details=exeptions.DontExistItemInsideDB().get_message,
                                  status=status.HTTP_404_NOT_FOUND, data=None)

        except ValidationError:
            return TReturnedModel(details=exeptions.UnknownExeptions().get_message,
                                  status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, data=None)

        except exeptions.UnknownExceptions:
            "HERE WE NEED PROVIDE LOGIC FOR ADDED TO DB"
            return TReturnedModel(details=exeptions.UnknownExeptions().get_message,
                                  status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, data=None)

    return wrapper
