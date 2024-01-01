import strawberry
from typing import Optional


@strawberry.type
class BasicExeptionsSchema:
    details: str
    status: int


class DoNotValidCredential(Exception):
    message = "You have entered an incorrect"

    def __init__(self, reason: Optional[str] = "password"):
        self.message = f"{self.message} {reason}!"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self) -> str:
        return self.message


class NoValidTokenRaw(Exception):
    message = "Your token is not valid. You are denied access!"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self) -> str:
        return self.message


class AlreadyExistInDB(Exception):
    message = "Already exists in the database!"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self) -> str:
        return self.message


class DoNotUpdateFieldsInDB(Exception):
    message = "We haven't been able to update fields in database!"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self) -> str:
        return self.message


class FailedCreate(Exception):
    def __init__(self, reason: str = " "):
        self.message = f"""You failed to create a {
            reason}. Try again in a little while."""

    def __str__(self, ) -> str:
        return self.message

    @property
    def get_message(self) -> str:
        return self.message


class YouDontHaveAccessExeptions(Exception):
    def __init__(self, reason: str = "!"):
        self.message = f"You don't have permission {reason}"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self,) -> str:
        return self.message


class DontExistItemInsideDB(Exception):
    message = "This object does not exist in the database!"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self) -> str:
        return self.message


class UnknownExceptions(Exception):
    message = "You have encountered an unknown error. We will contact you as soon as we have resolved this issue!"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self) -> str:
        return self.message


class StringWithLimit(Exception):
    def __init__(self, limit: int = 50):
        self.message = f"You passed a string that is too long. Must be less than or equal to {
            limit}!"

    def __str__(self) -> str:
        return self.message

    @property
    def get_message(self,) -> str:
        return self.message
