import strawberry


@strawberry.type
class BasicExeptionsSchema:
    details: str
    status: int


class NoValidTokenRaw(Exception):
    def __str__(self) -> str:
        return "No valid token."

    @property
    def get_message(self) -> str:
        return "No valid token."


class AlreadyExistInDB(Exception):
    def __str__(self) -> str:
        return "Already exists in the database!"

    @property
    def get_message(self) -> str:
        return "Already exists in the database!"


class DoNotUpdateFieldsInDB(Exception):
    def __str__(self) -> str:
        return "We haven't been able to update fields in database."

    @property
    def get_message(self) -> str:
        return "We haven't been able to update fields in database."


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


class UnknownExceptions(Exception):
    def __str__(self) -> str:
        return "You have encountered an unknown error. We will contact you as soon as we have resolved this issue."

    @property
    def get_message(self) -> str:
        return "You have encountered an unknown error. We will contact you as soon as we have resolved this issue."
