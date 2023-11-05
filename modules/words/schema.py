import strawberry
from typing import Optional, Union, Annotated
from dataclasses import field
from enum import Enum

from core.exeptions.ExeptionsSchema import BasicExeptionsSchema
from utils.params_helpers import ReturnedWithCommanParams


@strawberry.enum
class PartOfSpeach(str, Enum):
    NOUN = "NOUN"
    PRONOUN = "PRONOUN"
    VERB = "VERB"
    ADJECTIVE = "ADJECTIVE"
    ADVERB = "ADVERB"
    PREPOSITION = "PREPOSITION"
    CONJUNCTION = "CONJUNCTION"
    INTERJECTION = "INTERJECTION"


@strawberry.type
class Word:
    id: int
    slug: Optional[str] = field(default_factory=str)
    name: str
    example: Optional[str] = field(default_factory=str)
    translate: str
    synonym: Optional[list[str]] = field(default_factory=list)
    part_of_speach: PartOfSpeach
    image_url: Optional[str] = None


@strawberry.type
class ReturnedWordsType(ReturnedWithCommanParams):
    data: list[Word]


@strawberry.type
class ReturnedWordsFail:
    details: str
    status_code: int


@strawberry.type
class ReturnWordCreatedFail(BasicExeptionsSchema):
    pass


@strawberry.type
class ReturnWordCreatedType(BasicExeptionsSchema):
    word: Word


ReturnCreatedWordExtend = Annotated[
    Union[ReturnWordCreatedType, ReturnWordCreatedFail], strawberry.union("ReturnWordCreated")]


ReturnedWordsExtend = Annotated[Union[ReturnedWordsType,
                                      ReturnedWordsFail], strawberry.union("ReturnedWords")]
