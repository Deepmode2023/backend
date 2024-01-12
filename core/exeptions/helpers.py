from . import schema as exeptions
from fastapi import status
from core.schema.schemas import TReturnedFailed
from functools import wraps

from core.type import ExceptionResponseAPI, ResponseType


responses_status_errors = {404: {"model": ResponseType,
                                 "description": exeptions.DoNotUpdateFieldsInDB().get_message},
                           400: {"model": ResponseType,
                                 "description": exeptions.NoValidTokenRaw().get_message},

                           403: {"model": ResponseType,
                                 "description": exeptions.YouDontHaveAccessExeptions().get_message},
                           409: {"model": ResponseType,
                                 "description": exeptions.AlreadyExistInDB().get_message},
                           451: {"model": ResponseType,
                                 "description": exeptions.UnknownExceptions().get_message},
                           }


def exeption_handling_decorator(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)

        # BASIC EXEPTIONS
        except exeptions.DoNotUpdateFieldsInDB:
            return ExceptionResponseAPI(msg=exeptions.DoNotUpdateFieldsInDB().get_message,
                                        input={},
                                        reason=exeptions.DoNotUpdateFieldsInDB().get_message,
                                        status_code=status.HTTP_404_NOT_FOUND)

        except exeptions.NoValidTokenRaw:
            return ExceptionResponseAPI(msg=exeptions.NoValidTokenRaw().get_message,
                                        input={},
                                        reason=exeptions.NoValidTokenRaw().get_message,
                                        status_code=status.HTTP_400_BAD_REQUEST,
                                        header={"Authorization": "Bearer"})

        except exeptions.YouDontHaveAccessExeptions as permission_denied:
            return ExceptionResponseAPI(msg=permission_denied.get_message,
                                        input={},
                                        reason=permission_denied.get_message,
                                        status_code=status.HTTP_403_FORBIDDEN)

        except exeptions.DontExistItemInsideDB:
            return ExceptionResponseAPI(msg=exeptions.DontExistItemInsideDB().get_message,
                                        input={},
                                        reason=exeptions.DontExistItemInsideDB().get_message,
                                        status_code=status.HTTP_404_NOT_FOUND)

        except exeptions.AlreadyExistInDB:
            return ExceptionResponseAPI(msg=exeptions.AlreadyExistInDB().get_message,
                                        input={},
                                        reason=exeptions.AlreadyExistInDB().get_message,
                                        status_code=status.HTTP_409_CONFLICT)

        except exeptions.FailedCreate as failedException:
            return ExceptionResponseAPI(msg=failedException.get_message,
                                        input={},
                                        reason=failedException.get_message,
                                        status_code=status.HTTP_409_CONFLICT)

        except exeptions.DoNotValidCredential as validCredential:
            return ExceptionResponseAPI(msg=validCredential.get_message,
                                        input={},
                                        reason=validCredential.get_message,
                                        status_code=status.HTTP_401_UNAUTHORIZED,
                                        header={"Authorization": "Bearer"})

        except exeptions.UnknownExceptions:

            print(exeptions.UnknownExceptions().get_message, "<<<<<<")
            "HERE WE NEED PROVIDE LOGIC FOR ADDED TO DB"
            return ExceptionResponseAPI(msg=exeptions.UnknownExceptions().get_message,
                                        input={},
                                        reason=exeptions.UnknownExceptions().get_message,
                                        status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
        except Exception as ex:

            print(ex, "<<<<<<")
            "HERE WE NEED PROVIDE LOGIC FOR ADDED TO DB"
            return ExceptionResponseAPI(msg=exeptions.UnknownExceptions().get_message,
                                        input={},
                                        reason=exeptions.UnknownExceptions().get_message,
                                        status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
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

        except exeptions.DoNotValidCredential as validCredential:
            return TReturnedFailed(details=validCredential.get_message,
                                   status=status.HTTP_401_UNAUTHORIZED, data=[])

        except exeptions.StringWithLimit as stringWithLimit:
            return TReturnedFailed(details=stringWithLimit.get_message,
                                   status=status.HTTP_400_BAD_REQUEST, data=[])

        except exeptions.UnknownExceptions as exeption:
            "HERE WE NEED PROVIDE LOGIC FOR ADDED TO DB"
            print("=====> ", exeption)
            return TReturnedFailed(details=exeptions.UnknownExceptions().get_message,
                                   status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

    return wrapper
