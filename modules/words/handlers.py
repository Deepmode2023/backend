import strawberry
from strawberry.types import Info
from typing import Optional

from utils.params_helpers import CommonParams
from utils.math import calculate_pagination_page
from utils.security import JWTAuth
from db.session import get_db
from fastapi import status as StatusFastApi

from . import constants as constantPoint
from . import schema as SchemaInstanceType
from .dals import WordDAL


@strawberry.type
class Mutation:
    @strawberry.mutation(name=constantPoint.CREATE_WORD.get("name", ""), description=constantPoint.CREATE_WORD.get("descriptions", ""), permission_classes=[JWTAuth])
    async def create_word(self, info: Info, name: str, part_of_speach: SchemaInstanceType.PartOfSpeach, translate: str, slug: Optional[str] = "", example: Optional[str] = "", synonym: Optional[str] = [], image_url: Optional[str] = None) -> SchemaInstanceType.ReturnCreatedWordExtend:
        try:
            async with await anext(get_db()) as db_session:
                dals = WordDAL(db_session=db_session)
                created_word_instance = await dals.create_word(token_raw=info.context.get_raw_token, translate=translate, slug=slug,
                                                               name=name, example=example, synonym=synonym,
                                                               image_url=image_url,
                                                               part_of_speach=part_of_speach)
                return SchemaInstanceType.ReturnWordCreatedType(details="The word was successfully created.", status_code=StatusFastApi.HTTP_201_CREATED, word=created_word_instance)
        except Exception:
            return SchemaInstanceType.ReturnWordCreatedFail(details="The word was already created.", status_code=StatusFastApi.HTTP_409_CONFLICT)

    @strawberry.mutation(name=constantPoint.UPDATE_WORD.get("name", ""), description=constantPoint.UPDATE_WORD.get("descriptions", ""), permission_classes=[JWTAuth])
    async def update_word(self, info: Info, name: Optional[str] = None, part_of_speach: Optional[SchemaInstanceType.PartOfSpeach] = None, translate: Optional[str] = None, slug: Optional[str] = None, example: Optional[str] = None, synonym: Optional[str] = None, image_url: Optional[str] = None) -> SchemaInstanceType.ReturnCreatedWordExtend:
        pass


@strawberry.type
class Query:
    @strawberry.field(name=constantPoint.GET_WORDS.get("name", ""), description=constantPoint.GET_WORDS.get("descriptions", ""), permission_classes=[JWTAuth])
    async def get_words(self, common_params: CommonParams = {}) -> SchemaInstanceType.ReturnedWordsExtend:
        try:
            async with await anext(get_db()) as db_session:
                dals = WordDAL(db_session=db_session)
                words = await dals.get_words(commonParams=common_params)
                pagination_count = calculate_pagination_page(
                    limmit=common_params.limit, skip=common_params.skip)

                return SchemaInstanceType.ReturnedWordsType(
                    limmit=common_params.limit,
                    pagination=pagination_count,
                    skip=common_params.skip,
                    data=words
                )
        except Exception:
            return SchemaInstanceType.ReturnedWordsFail(details="Failed", status_code=404)
