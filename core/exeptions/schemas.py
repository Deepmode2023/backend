import strawberry


@strawberry.type
class BasicExeptionsSchema:
    details: str
    status: int


class NoValidTokenRaw(Exception):
    def __str__(self) -> str:
        return "Your token is not valid. You are denied access!"

    @property
    def get_message(self) -> str:
        return "Your token is not valid. You are denied access!"


class AlreadyExistInDB(Exception):
    def __str__(self) -> str:
        return "Already exists in the database!"

    @property
    def get_message(self) -> str:
        return "Already exists in the database!"


class DoNotUpdateFieldsInDB(Exception):
    def __str__(self) -> str:
        return "We haven't been able to update fields in database!"

    @property
    def get_message(self) -> str:
        return "We haven't been able to update fields in database!"


class FailedCreate(Exception):
    def __init__(self, issue: str = " "):
        self.issue = f"a {issue}"

    def __str__(self, ) -> str:
        return f"You failed to create {self.issue}! Try again in a little while."

    @property
    def get_message(self) -> str:
        return f"You failed to create {self.issue}! Try again in a little while."


class YouDontHaveAccessExeptions(Exception):
    def __init__(self, reason: str = "!"):
        self.reason = reason

    def __str__(self) -> str:
        return f"You don't have permission {self.reason}"

    @property
    def get_message(self,) -> str:
        return f"You don't have permission {self.reason}"


class DontExistItemInsideDB(Exception):
    def __str__(self) -> str:
        return "This object does not exist in the database!"

    @property
    def get_message(self) -> str:
        return "This object does not exist in the database!"


class UnknownExceptions(Exception):
    def __str__(self) -> str:
        return "You have encountered an unknown error. We will contact you as soon as we have resolved this issue!"

    @property
    def get_message(self) -> str:
        return "You have encountered an unknown error. We will contact you as soon as we have resolved this issue!"
