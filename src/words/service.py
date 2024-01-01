import strawberry
from typing import Optional
from strawberry.types import Info

from utils.params_helpers import CommonParams
from utils.math import calculate_pagination_page
from db.session import get_session
from fastapi import status as StatusFastApi
from utils.security import JWTAuth


from . import constants as constantPoint
from . import schema as SchemaInstanceType
from .dals import WordDAL
from core.exeptions.helpers import exeption_handling_decorator_graph_ql


from typing import Annotated, cast, Type
from pydantic import GetJsonSchemaHandler, BaseModel
from pydantic_core.core_schema import JsonSchema, with_info_plain_validator_function
from pydantic_core import CoreSchema, core_schema
from typing import Any, Callable


class Zima:
    @classmethod
    def _validate(cls, __input_value: Any, _: Any) -> bool:
        print(__input_value)
        return cast(str, __input_value)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchema:

        return {"type": "string", "format": "color"}

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        return with_info_plain_validator_function(cls._validate)


@strawberry.type
class Mutation:
    @strawberry.mutation(name=constantPoint.UPDATE_WORD["name"],
                         description=constantPoint.UPDATE_WORD["descriptions"])
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
                         description=constantPoint.DELETE_WORD["descriptions"])
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
