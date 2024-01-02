import strawberry
from fastapi import status
from strawberry.types import Info
from typing import Optional
from datetime import datetime

from utils.security import JWTAuth
from .constants import POST_SPACED_REPETITION, DELETE_SPACED_REPETITION, GET_SPACED_REPETITION
from .dals import SpacedRepetitionDAL

from . import schema as spaced_schema

from db.session import get_session

from core.exeptions.helpers import exeption_handling_decorator_graph_ql
from core.exeptions.schema import StringWithLimit


@strawberry.type
class Mutation:
    @strawberry.mutation(name=POST_SPACED_REPETITION.get("name"),
                         description=POST_SPACED_REPETITION.get("description"), permission_classes=[JWTAuth])
    @exeption_handling_decorator_graph_ql
    async def post_spaced_repetition(self, info: Info, description: str, slug: spaced_schema.SlugEnum, title: str, condition_repetition: bool = True) -> spaced_schema.ReturnedSpacedRepetitionPostType:
        try:
            if len(title) > 50:
                raise StringWithLimit(limit=50)

            current_user = info.context.current_user
            async with get_session() as db_session:
                dals = SpacedRepetitionDAL(db_session=db_session)
                returned_data = await dals.post_spaced_repetition(current_user=current_user,
                                                                  description=description,
                                                                  slug=slug,
                                                                  title=title,
                                                                  condition_repetition=condition_repetition)

                return spaced_schema.ReturnedSpacedRepetition(details=POST_SPACED_REPETITION.get("success"), status=status.HTTP_200_OK, data=spaced_schema.SpacedRepetitionResponse(**returned_data.toJson))
        except Exception:
            raise

    @strawberry.mutation(name=DELETE_SPACED_REPETITION.get("name"),
                         description=DELETE_SPACED_REPETITION.get("description"), permission_classes=[JWTAuth])
    @exeption_handling_decorator_graph_ql
    async def delete_spaced_repetition(self, info: Info, id: int) -> spaced_schema.ReturnedSpacedRepetitionDeleteType:
        try:
            current_user = info.context.current_user
            async with get_session() as db_session:
                dals = SpacedRepetitionDAL(db_session=db_session)
                returned_data = await dals.delete_spaced_repetition(current_user=current_user, id=id)

                return spaced_schema.ReturnedSpacedRepetition(details=f"{DELETE_SPACED_REPETITION.get('success')} with ID={id}!",
                                                              status=status.HTTP_200_OK,
                                                              data=spaced_schema.SpacedRepetitionResponse(**returned_data.toJson))
        except Exception:
            raise


@strawberry.type
class Query:
    @strawberry.field(name=GET_SPACED_REPETITION.get("name"),
                      description=GET_SPACED_REPETITION.get("description"), permission_classes=[JWTAuth])
    @exeption_handling_decorator_graph_ql
    async def get_spaced_repetition(self, info: Info, date_start: datetime,
                                    date_end: datetime, slug: Optional[spaced_schema.SlugEnum] = None, title: Optional[str] = None) -> spaced_schema.ReturnedSpacedRepetitionGetType:
        try:
            current_user = info.context.current_user
            async with get_session() as db_session:
                dals = SpacedRepetitionDAL(db_session=db_session)
                returned_data = await dals.get_spaced_repetition(current_user=current_user, date_start=date_start,
                                                                 date_end=date_end, slug=slug, title=title)
                return spaced_schema.ReturnedSpacedRepetitionList(details=GET_SPACED_REPETITION.get("success"),
                                                                  status=status.HTTP_200_OK, data=[spaced_schema.SpacedRepetitionResponse(**model.toJson) for model in returned_data])
        except Exception:
            raise
