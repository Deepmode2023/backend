import strawberry
from fastapi import status


@strawberry.type
class BasicExeptionsSchema:
    details: str
    status_code: int
