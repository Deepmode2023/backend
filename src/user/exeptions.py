

class DontAllowChangeUser(Exception):
    def __str__(self) -> str:
        return "You are not allowed to change the user metadata because not enough time has passed. Try again 1 day after the last update date."

    @property
    def get_message(self) -> str:
        return "You are not allowed to change the user metadata because not enough time has passed. Try again 1 day after the last update date."
