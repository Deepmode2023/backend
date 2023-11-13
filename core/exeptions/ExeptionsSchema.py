import strawberry
from fastapi import status


@strawberry.type
class BasicExeptionsSchema:
    details: str
    status_code: int


class YouDontHaveAccessExeptions(Exception):
    def __str__(self) -> str:
        return "You don't have permission to delete words."

    @property
    def get_message(self) -> str:
        return "You don't have permission to delete words."


class DontExistItemInsideDB(Exception):
    def __str__(self) -> str:
        return "This object does not exist in the database."

    @property
    def get_message(self) -> str:
        return "This object does not exist in the database."


class UnknownExeptions(Exception):
    def __str__(self) -> str:
        return "You have encountered an unknown error. We will contact you as soon as we have resolved this issue."

    @property
    def get_message(self) -> str:
        return "You have encountered an unknown error. We will contact you as soon as we have resolved this issue."
