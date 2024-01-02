import strawberry
from enum import Enum
from typing import Union, Annotated
from datetime import datetime


from core.exeptions.schema import BasicExceptionSchema
from core.schema.schemas import TReturnedFailed


@strawberry.enum
class SlugEnum(str, Enum):
    WORD = "word"
    PDF = "pdf"
    THEME_WITH_SLANG = "theme_with_slang"


@strawberry.type
class SpacedRepetitionResponse:
    def __init__(cls, **kwargs):
        cls.id = kwargs.get("id")
        cls.slug = kwargs.get("slug")
        cls.title = kwargs.get("title")
        cls.description = kwargs.get("description")
        cls.date_repetition = kwargs.get("date_repetition")
        cls.date_last_repetition = kwargs.get("date_last_repetition")

    id: int
    slug: str
    title: str
    description: str
    date_repetition: datetime
    date_last_repetition: datetime


@strawberry.type
class ReturnedSpacedRepetition(BasicExceptionSchema):
    data: SpacedRepetitionResponse


@strawberry.type
class ReturnedSpacedRepetitionList(BasicExceptionSchema):
    data: list[SpacedRepetitionResponse]


ReturnedSpacedRepetitionPostType = Annotated[Union[ReturnedSpacedRepetition,
                                                   TReturnedFailed], strawberry.union("ReturnedSpacedRepetitionPost")]


ReturnedSpacedRepetitionDeleteType = Annotated[Union[ReturnedSpacedRepetition,
                                                     TReturnedFailed], strawberry.union("ReturnedSpacedRepetitionDelete")]

ReturnedSpacedRepetitionGetType = Annotated[Union[ReturnedSpacedRepetitionList,
                                                  TReturnedFailed], strawberry.union("ReturnedSpacedRepetitionGet")]
