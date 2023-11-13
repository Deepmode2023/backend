from pydantic import BaseModel


class TotalReturnedModel(BaseModel):
    detail: str
    status: int
    data: list
