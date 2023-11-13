

class NotFieldExist(Exception):
    def __str__(self) -> str:
        return "No such key exists in this object."
