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


# GET WORDS BLOCK


@strawberry.type
class ReturnedWordsType(ReturnedWithCommanParams):
    data: list[Word]


@strawberry.type
class ReturnedWordsFail:
    details: str
    status_code: int


ReturnWordsExtendType = Annotated[Union[ReturnedWordsType,
                                        ReturnedWordsFail], strawberry.union("ReturnedWords")]
# END GET WORDS BLOCK

# CREATE WORD BLOCK


@strawberry.type
class ReturnWordCreatedFail(BasicExeptionsSchema):
    pass


@strawberry.type
class ReturnWordCreatedType(BasicExeptionsSchema):
    data: list[Word]


ReturnCreatedWordExtendType = Annotated[
    Union[ReturnWordCreatedType, ReturnWordCreatedFail], strawberry.union("ReturnWordCreated")]
# END CREATE WORD BLOCK

# UPDATE WORD BLOCK


@strawberry.type
class ReturnWordUpdatedType(BasicExeptionsSchema):
    data: list[Word]


@strawberry.type
class ReturnWordUpdatedFail(BasicExeptionsSchema):
    pass


ReturnUpdatedWordExtendType = Annotated[
    Union[ReturnWordUpdatedType, ReturnWordUpdatedFail], strawberry.union("ReturnWordUpgrade")]

# END UPDATE WORD BLOCK


# DELETE WORD BLOCK

@strawberry.type
class ReturnWordDeleteType(BasicExeptionsSchema):
    data: Word


@strawberry.type
class ReturnWordDeleteFail(BasicExeptionsSchema):
    pass


ReturnDeleteWordExtendType = Annotated[
    Union[ReturnWordDeleteType, ReturnWordDeleteFail], strawberry.union("ReturnWordDelete")]

# END DELETE WORD BLOCK
