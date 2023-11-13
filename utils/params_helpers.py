import strawberry
from typing import Optional


def common_params(pagination: int = 0, skip: int = 0, limit: int = 10) -> dict:
    return {"pagination": pagination, "skip": skip, "limit": limit}


@strawberry.input
class CommonParams:
    pagination: Optional[int] = 1
    limit: Optional[int] = 50
    skip: Optional[int] = 0


@strawberry.type
class ReturnedWithCommanParams:
    limmit: int
    pagination: int
    skip: int
