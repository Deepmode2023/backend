import strawberry
from typing import Optional
from strawberry.types import Info

from utils.params_helpers import CommonParams
from utils.math import calculate_pagination_page
from db.session import get_session
from fastapi import status as StatusFastApi
from utils.security import JWTAuth
from utils.basic import build_kwargs_not_none


from . import constants as constantPoint
from . import schema as SchemaInstanceType
from .dals import WordDAL
from core.exeptions.helpers import exeption_handling_decorator_graph_ql


@strawberry.type
class Mutation:

    @strawberry.mutation(name=constantPoint.CREATE_WORD["name"],
                         description=constantPoint.CREATE_WORD["descriptions"], permission_classes=[JWTAuth])
    @exeption_handling_decorator_graph_ql
    async def create_word(self, info: Info,
                          name: str, part_of_speach: SchemaInstanceType.PartOfSpeach,
                          translate: str, slug: str, example: Optional[str] = "",
                          slang: Optional[SchemaInstanceType.SlangEnum] = SchemaInstanceType.SlangEnum.ENG,
                          synonym: Optional[list[str]] = [], image_url: Optional[str] = None) -> SchemaInstanceType.ReturnCreatedWordExtendType:
        try:
            current_user = info.context.current_user
            async with get_session() as db_session:
                words_kwargs = build_kwargs_not_none(slang=slang, name=name,
                                                     translate=translate, part_of_speach=part_of_speach, slug=slug,
                                                     example=example, synonym=synonym, image_url=image_url)
                dals = WordDAL(db_session=db_session)
                created_word = await dals.create_word(current_user=current_user, **words_kwargs)

                return SchemaInstanceType.ReturnWordCreatedType(details=f"Successfuly created word with ID={created_word.id}",
                                                                status=StatusFastApi.HTTP_201_CREATED, data=SchemaInstanceType.Word(**created_word.toJson))

        except Exception:
            raise

    @strawberry.mutation(name=constantPoint.UPDATE_WORD["name"],
                         description=constantPoint.UPDATE_WORD["descriptions"], permission_classes=[JWTAuth])
    @exeption_handling_decorator_graph_ql
    async def update_word(self, info: Info, id: int,
                          slang: Optional[SchemaInstanceType.SlangEnum] = SchemaInstanceType.SlangEnum.ENG,
                          name: Optional[str] = None, part_of_speach: Optional[SchemaInstanceType.PartOfSpeach] = None,
                          translate: Optional[str] = None, slug: Optional[str] = None, example: Optional[str] = None,
                          synonym: Optional[str] = None, image_url: Optional[str] = None) -> SchemaInstanceType.ReturnUpdatedWordExtendType:
        try:
            current_user = info.context.current_user
            async with get_session() as db_session:
                dals = WordDAL(db_session=db_session)
                updated_word_instance = await dals.update_word(id=id, user=current_user, translate=translate, slug=slug,
                                                               name=name, example=example, synonym=synonym,
                                                               slang=slang,
                                                               image_url=image_url,
                                                               part_of_speach=part_of_speach)

                return SchemaInstanceType.ReturnWordUpdatedType(details="You've been successful in updating the word.",
                                                                status=StatusFastApi.HTTP_200_OK, data=[updated_word_instance])
        except Exception:
            raise

    @strawberry.mutation(name=constantPoint.DELETE_WORD["name"],
                         description=constantPoint.DELETE_WORD["descriptions"], permission_classes=[JWTAuth])
    @exeption_handling_decorator_graph_ql
    async def delete_word(self, info: Info, id: int) -> SchemaInstanceType.ReturnDeleteWordExtendType:
        try:
            current_user = info.context.current_user
            async with get_session() as db_session:
                dals = WordDAL(db_session=db_session)
                delete_word = await dals.delete_word(id=id, user=current_user)
            return SchemaInstanceType.ReturnWordDeleteType(details="You've been successful in delete the word.",
                                                           status=StatusFastApi.HTTP_200_OK, data=delete_word)
        except Exception:
            raise


@strawberry.type
class Query:
    @strawberry.field(name=constantPoint.GET_WORDS["name"],
                      description=constantPoint.GET_WORDS["descriptions"])
    @exeption_handling_decorator_graph_ql
    async def get_words(info: Info, common_params: CommonParams = {},
                        slug: Optional[str] = None, name: Optional[str] = None) -> SchemaInstanceType.ReturnWordsExtendType:
        try:
            async with get_session() as db_session:
                dals = WordDAL(db_session=db_session)

                if slug != None or name != None:
                    words = await dals.get_words_by_slug_or_name(commonParams=common_params, name=name, slug=slug)
                else:
                    words = await dals.get_words(commonParams=common_params)

                pagination_count = calculate_pagination_page(
                    limmit=common_params.limmit, skip=common_params.skip)

                return SchemaInstanceType.ReturnedWordsType(
                    limmit=common_params.limmit,
                    pagination=pagination_count,
                    skip=common_params.skip,
                    data=words
                )
        except Exception:
            raise
