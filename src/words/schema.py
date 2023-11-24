import strawberry
from typing import Optional, Union, Annotated
from dataclasses import field
from enum import Enum

from core.exeptions.schemas import BasicExeptionsSchema
from core.schema.schemas import TReturnedFailed
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


@strawberry.enum
class SlangEnum(str, Enum):
    ENG = "england"
    USA = "united states"
    PL = "poland"


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


# GET WORDS BLOCK


@strawberry.type
class ReturnedWordsType(ReturnedWithCommanParams):
    data: list[Word]


ReturnWordsExtendType = Annotated[Union[ReturnedWordsType,
                                        TReturnedFailed], strawberry.union("ReturnedWords")]
# END GET WORDS BLOCK

# CREATE WORD BLOCK


@strawberry.type
class ReturnWordCreatedType(BasicExeptionsSchema):
    data: list[Word]


ReturnCreatedWordExtendType = Annotated[
    Union[ReturnWordCreatedType, TReturnedFailed], strawberry.union("ReturnWordCreated")]
# END CREATE WORD BLOCK

# UPDATE WORD BLOCK


@strawberry.type
class ReturnWordUpdatedType(BasicExeptionsSchema):
    data: list[Word]


ReturnUpdatedWordExtendType = Annotated[
    Union[ReturnWordUpdatedType, TReturnedFailed], strawberry.union("ReturnWordUpgrade")]

# END UPDATE WORD BLOCK


# DELETE WORD BLOCK

@strawberry.type
class ReturnWordDeleteType(BasicExeptionsSchema):
    data: Word


ReturnDeleteWordExtendType = Annotated[
    Union[ReturnWordDeleteType, TReturnedFailed], strawberry.union("ReturnWordDelete")]

# END DELETE WORD BLOCK
