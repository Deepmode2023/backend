from pydantic import BaseModel
from typing import Union, Dict, Any
import strawberry


class TReturnedModel(BaseModel):
    details: str
    status: int
    data:  Union[list[Dict[str, Any]], None]


@strawberry.type
class BasicExeptionsSchema:
    details: str
    status_code: int
