from . import schemas as exeptions
from fastapi import status
from core.schema.schemas import TReturnedModel, TReturnedFailed
from functools import wraps


def exeption_handling_decorator(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)

        # BASIC EXEPTIONS
        except exeptions.DoNotUpdateFieldsInDB:
            return TReturnedModel(details=exeptions.DoNotUpdateFieldsInDB().get_message,
                                  status=status.HTTP_404_NOT_FOUND, data=[])

        except exeptions.NoValidTokenRaw:
            return TReturnedModel(details=exeptions.NoValidTokenRaw().get_message,
                                  status=status.HTTP_400_BAD_REQUEST, data=[])

        except exeptions.YouDontHaveAccessExeptions:
            return TReturnedModel(details=exeptions.YouDontHaveAccessExeptions().get_message,
                                  status=status.HTTP_401_UNAUTHORIZED, data=[])

        except exeptions.DontExistItemInsideDB:
            return TReturnedModel(details=exeptions.DontExistItemInsideDB().get_message,
                                  status=status.HTTP_404_NOT_FOUND, data=[])

        except exeptions.AlreadyExistInDB:
            return TReturnedModel(details=exeptions.AlreadyExistInDB().get_message,
                                  status=status.HTTP_409_CONFLICT, data=[])

        except exeptions.UnknownExceptions as exe:
            "HERE WE NEED PROVIDE LOGIC FOR ADDED TO DB"
            return TReturnedModel(details=exeptions.UnknownExceptions().get_message,
                                  status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, data=[])

    return wrapper


def exeption_handling_decorator_graph_ql(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)

        # BASIC EXEPTIONS
        except exeptions.DoNotUpdateFieldsInDB:
            return TReturnedFailed(details=exeptions.DoNotUpdateFieldsInDB().get_message,
                                   status=status.HTTP_404_NOT_FOUND)

        except exeptions.NoValidTokenRaw:
            return TReturnedFailed(details=exeptions.NoValidTokenRaw().get_message,
                                   status=status.HTTP_400_BAD_REQUEST)

        except exeptions.YouDontHaveAccessExeptions:
            return TReturnedFailed(details=exeptions.YouDontHaveAccessExeptions().get_message,
                                   status=status.HTTP_401_UNAUTHORIZED)

        except exeptions.DontExistItemInsideDB:
            return TReturnedFailed(details=exeptions.DontExistItemInsideDB().get_message,
                                   status=status.HTTP_404_NOT_FOUND)

        except exeptions.AlreadyExistInDB:
            return TReturnedFailed(details=exeptions.AlreadyExistInDB().get_message,
                                   status=status.HTTP_409_CONFLICT)

        except exeptions.UnknownExceptions as exeption:
            "HERE WE NEED PROVIDE LOGIC FOR ADDED TO DB"
            print("=====> ", exeption)
            return TReturnedFailed(details=exeptions.UnknownExceptions().get_message,
                                   status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

    return wrapper
