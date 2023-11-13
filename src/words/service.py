import strawberry
from strawberry.types import Info
from typing import Optional

from utils.params_helpers import CommonParams
from utils.math import calculate_pagination_page
from utils.security import JWTAuth
from db.session import get_db, get_session
from fastapi import status as StatusFastApi

from . import constants as constantPoint
from . import schema as SchemaInstanceType
from .dals import WordDAL
from core.exeptions import ExeptionsSchema as core_exeptions


@strawberry.type
class Mutation:
    @strawberry.mutation(name=constantPoint.CREATE_WORD["name"],
                         description=constantPoint.CREATE_WORD["descriptions"], permission_classes=[JWTAuth])
    async def create_word(self, info: Info, name: str, part_of_speach: SchemaInstanceType.PartOfSpeach,
                          translate: str, slug: Optional[str] = "", example: Optional[str] = "",
                          synonym: Optional[str] = [], image_url: Optional[str] = None) -> SchemaInstanceType.ReturnCreatedWordExtendType:
        try:
            async with await anext(get_db()) as db_session:
                dals = WordDAL(db_session=db_session)
                created_word_instance = await dals.create_word(token_raw=info.context.get_raw_token, translate=translate, slug=slug,
                                                               name=name, example=example, synonym=synonym,
                                                               image_url=image_url,
                                                               part_of_speach=part_of_speach)
                return SchemaInstanceType.ReturnWordCreatedType(details="The word was successfully created.",
                                                                status_code=StatusFastApi.HTTP_201_CREATED, data=[created_word_instance])
        except Exception:
            print("ADD HERE ADD TO BD TRACER EXEPTIONS")
            return SchemaInstanceType.ReturnWordCreatedFail(details="The word was already created.",
                                                            status_code=StatusFastApi.HTTP_409_CONFLICT)

    @strawberry.mutation(name=constantPoint.UPDATE_WORD["name"],
                         description=constantPoint.UPDATE_WORD["descriptions"], permission_classes=[JWTAuth])
    async def update_word(self, info: Info, id: int,
                          name: Optional[str] = None, part_of_speach: Optional[SchemaInstanceType.PartOfSpeach] = None,
                          translate: Optional[str] = None, slug: Optional[str] = None, example: Optional[str] = None,
                          synonym: Optional[str] = None, image_url: Optional[str] = None) -> SchemaInstanceType.ReturnUpdatedWordExtendType:
        try:
            async with get_session() as db_session:
                dals = WordDAL(db_session=db_session)
                updated_word_instance = await dals.update_word(id=id, token_raw=info.context.get_raw_token, translate=translate, slug=slug,
                                                               name=name, example=example, synonym=synonym,
                                                               image_url=image_url,
                                                               part_of_speach=part_of_speach)

                return SchemaInstanceType.ReturnWordUpdatedType(details="You've been successful in updating the word.",
                                                                status_code=StatusFastApi.HTTP_200_OK, data=[updated_word_instance])

        except core_exeptions.DontExistItemInsideDB:
            return SchemaInstanceType.ReturnWordUpdatedFail(details="The word with this id does not exist in the database.",
                                                            status_code=StatusFastApi.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            print("ADD HERE ADD TO BD TRACER EXEPTIONS")
            return SchemaInstanceType.ReturnWordUpdatedFail(details="The server crashed for some unknown reason.",
                                                            status_code=StatusFastApi.HTTP_400_BAD_REQUEST)

    @strawberry.mutation(name=constantPoint.DELETE_WORD["name"],
                         description=constantPoint.DELETE_WORD["descriptions"], permission_classes=[JWTAuth])
    async def delete_word(self, info: Info, id: int) -> SchemaInstanceType.ReturnDeleteWordExtendType:
        try:
            async with get_session() as db_session:
                dals = WordDAL(db_session=db_session)
                delete_word = await dals.delete_word(
                    id=id, token_raw=info.context.get_raw_token)
            return SchemaInstanceType.ReturnWordDeleteType(details="You've been successful in delete the word.",
                                                           status_code=StatusFastApi.HTTP_200_OK, data=delete_word)
        except core_exeptions.YouDontHaveAccessExeptions:
            return SchemaInstanceType.ReturnWordDeleteFail(
                details=core_exeptions.YouDontHaveAccessExeptions().get_message, status_code=StatusFastApi.HTTP_403_FORBIDDEN)
        except core_exeptions.DontExistItemInsideDB:
            return SchemaInstanceType.ReturnWordDeleteFail(
                details=core_exeptions.DontExistItemInsideDB().get_message, status_code=StatusFastApi.HTTP_403_FORBIDDEN)
        except Exception as ex:
            print("ADD HERE ADD TO BD TRACER EXEPTIONS", ex)
            return SchemaInstanceType.ReturnWordDeleteFail(
                details=core_exeptions.DontExistItemInsideDB().get_message, status_code=StatusFastApi.HTTP_403_FORBIDDEN)


@strawberry.type
class Query:
    @strawberry.field(name=constantPoint.GET_WORDS["name"],
                      description=constantPoint.GET_WORDS["descriptions"], permission_classes=[JWTAuth])
    async def get_words(self, common_params: CommonParams = {},
                        slug: Optional[str] = None, name: Optional[str] = None) -> SchemaInstanceType.ReturnWordsExtendType:
        try:
            async with await anext(get_db()) as db_session:
                dals = WordDAL(db_session=db_session)

                if slug != None or name != None:
                    words = await dals.get_words_by_slug_or_name(commonParams=common_params, name=name, slug=slug)
                else:
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