from src.user.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from dataclasses import dataclass
from typing import Union

from .models import SpacedRepetitionsModel
from .engine.spaced_repetitions_engine import SpacedRepetitionsEngine

from utils.basic import build_kwargs_not_none


@dataclass
class SpacedRepetitionDAL:
    def __init__(cls, db_session: AsyncSession):
        cls.db_session = db_session

    async def post_spaced_repetition(cls, current_user: UserModel, condition_repetition: bool, **spaced_model_args) -> SpacedRepetitionsModel:
        repetition_manager = await SpacedRepetitionsEngine.create(current_user=current_user, condition_repetition=condition_repetition, **spaced_model_args)

        return await repetition_manager.update_db_model()

    async def delete_spaced_repetition(cls, id: int, current_user: UserModel):
        return await SpacedRepetitionsEngine.delete_db_model(id=id, current_user=current_user)

    async def get_spaced_repetition(cls, current_user: UserModel, date_start: datetime,
                                    date_end: datetime, slug: Union[str, None], title: Union[str, None]):
        search_kwargs = build_kwargs_not_none(slug=slug, title=title)
        return await SpacedRepetitionsEngine.get_db_model(current_user=current_user, date_end=date_end, date_start=date_start, **search_kwargs)
