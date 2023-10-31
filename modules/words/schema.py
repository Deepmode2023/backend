import strawberry
from typing import Union
from enum import Enum


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
    slug: str
    name: str
    description: str
    synonym: Union[list[str], None]
    part_of_speach: PartOfSpeach
    image_url: Union[str, None]
