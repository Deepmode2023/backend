from pydantic import BaseModel

from typing import Union, Dict, Any
from core.exeptions.schemas import BasicExeptionsSchema


class TReturnedModel(BaseModel):
    details: str
    status: int
    data:  Union[list[Dict[str, Any]], None]


class TReturnedFailed(BasicExeptionsSchema):
    pass
