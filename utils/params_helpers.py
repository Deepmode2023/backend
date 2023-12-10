import strawberry
from typing import Optional


def common_params(pagination: int = 0, skip: int = 0, limmit: int = 50) -> dict:
    return {"pagination": pagination, "skip": skip, "limmit": limmit if limmit < 1000 else 1000}


@strawberry.input
class CommonParams:
    def __init__(self, pagination: Optional[int] = 1, limmit: Optional[int] = 50, skip: Optional[int] = 0):
        self.pagination = pagination
        self.limmit = limmit if limmit < 1000 else 1000
        self.skip = skip

    pagination: Optional[int]
    limmit: Optional[int]
    skip: Optional[int]


@strawberry.type
class ReturnedWithCommanParams:
    limmit: int
    pagination: int
    skip: int


def checked_params_on_none(**kwargs):
    return {key: value for key, value in kwargs.items() if value is not None}
