from datetime import datetime
from typing import Union, Optional
from sqlalchemy import select, update, insert, delete


from utils.time import TimeManager, RequestDateType
from utils.list import replacement_filter
from utils.dict import extract_key_or_value
from utils.security import is_admin_checked
from utils.uuid import compare_uuid
from .math import formula_spaced_repetition

from core.exeptions.schema import YouDontHaveAccessExeptions, DontExistItemInsideDB
from db.call import add_fetch_one_item, scalars_fetch_many, scalars_fetch_one_or_none
from src.spaced_repetitions.models import SpacedRepetitionsModel
from src.user.models import UserModel


class SpacedUserManager(TimeManager):
    def __init__(cls, current_user: UserModel):
        cls.current_user = current_user

    async def get_user_repetitions(cls, user: Optional[UserModel] = None) -> list[SpacedRepetitionsModel]:
        user = user if user else cls.current_user
        smtp = select(SpacedRepetitionsModel).where(
            SpacedRepetitionsModel.user_id == user.user_id)
        return await scalars_fetch_many(smtp)


class SpacedRepetitionsEngine(SpacedUserManager):
    model_exist_in_db = False
    spaced_model: Union[SpacedRepetitionsModel, None] = None
    condition_repetition = False

    def __init__(cls, current_user: UserModel, condition_repetition,  **spaced_model_params):
        super(SpacedRepetitionsEngine, cls).__init__(current_user)
        cls.condition_repetition = condition_repetition
        if spaced_model_params:
            cls._set_default_spaced_repetition(**spaced_model_params)

    @classmethod
    async def create(cls, current_user: UserModel,
                     condition_repetition: Optional[bool] = False, **spaced_model_params):
        engine_cls = cls(current_user=current_user,
                         condition_repetition=condition_repetition, **spaced_model_params)

        # Checked inside DB
        spaced_model_iside_db: Union[SpacedRepetitionsModel, None] = await engine_cls._spaced_model_inside_db()

        if spaced_model_iside_db:
            engine_cls._update_spaced_model(prev_model=spaced_model_iside_db)
            engine_cls.model_exist_in_db = True

        return engine_cls

    # TODO HELPERS METHOD

    def _update_spaced_model(cls, prev_model):
        cls.spaced_model = SpacedRepetitionsModel(**extract_key_or_value(
            prev_model.toJson, ["count_repetition", "date_last_repetition", "date_repetition"]),
            count_repetition=prev_model.count_repetition +
            1 if cls.condition_repetition else 1,
            date_last_repetition=cls.current_date,
            date_repetition=cls._calculate_repetition_day(prev_model=prev_model))

    def _calculate_repetition_day(cls, prev_model: Optional[SpacedRepetitionsModel] = None) -> datetime:
        updated_date = cls.current_date.add(days=1)
        # if you cant repeat you must repeat on the next day
        if not cls.condition_repetition:
            cls.set_new_date(RequestDateType(
                year=updated_date.year, month=updated_date.month, day=updated_date.day))
            return cls.get_date

         # else grep your count repetition and multiple it on the 2
        count_repetition = prev_model.count_repetition if prev_model is not None else cls.count_repetition

        updated_date = cls.current_date.add(
            days=formula_spaced_repetition(count_repetition))
        cls.set_new_date(RequestDateType(
            year=updated_date.year, month=updated_date.month, day=updated_date.day))
        return cls.get_date

    async def _spaced_model_inside_db(cls) -> Union[SpacedRepetitionsModel, None]:
        all_user_repetiotions: list[SpacedRepetitionsModel] = await cls.get_user_repetitions()
        return next((itter_model for itter_model in all_user_repetiotions if itter_model == cls.spaced_model), None)

    def _set_default_spaced_repetition(cls, **spaced_model_params):
        date_repetition = spaced_model_params.date_repetiotion if spaced_model_params.get(
            'date_repetiotion', None) else cls.current_date
        date_last_repetition = spaced_model_params.date_last_repetition if spaced_model_params.get(
            'date_last_repetition', None) else cls.current_date.add(days=1)

        cls.spaced_model = SpacedRepetitionsModel(date_repetition=date_repetition,
                                                  date_last_repetition=date_last_repetition,
                                                  count_repetition=0,
                                                  user_id=cls.current_user.user_id, **spaced_model_params)

    # TODO GETTER METHOD

    @property
    def get_spaced_model_in_dict(cls):
        return cls.spaced_model.toJson

    # TODO ACTION METHOD

    async def update_db_model(cls):
        smpt = insert(SpacedRepetitionsModel).values(
            **extract_key_or_value(cls.get_spaced_model_in_dict, ['id'])).returning(SpacedRepetitionsModel)

        if cls.model_exist_in_db:
            smpt = update(SpacedRepetitionsModel).where(
                SpacedRepetitionsModel.id == cls.spaced_model.id).values(**cls.get_spaced_model_in_dict).returning(SpacedRepetitionsModel)

        return await add_fetch_one_item(smpt)

    @classmethod
    async def delete_db_model(cls, id: int, current_user: UserModel) -> SpacedRepetitionsModel:
        deleted_model = await scalars_fetch_one_or_none(select(SpacedRepetitionsModel).where(SpacedRepetitionsModel.id == id))
        if is_admin_checked(roles=current_user.roles) or deleted_model and compare_uuid(current_user.user_id, deleted_model.user_id):
            smpt = delete(SpacedRepetitionsModel).where(
                SpacedRepetitionsModel.id == deleted_model.id).returning(SpacedRepetitionsModel)
            return await add_fetch_one_item(smpt)

        if not deleted_model:
            raise DontExistItemInsideDB
        raise YouDontHaveAccessExeptions(reason="for delete this repetition!")

    @classmethod
    async def get_db_model(cls, current_user: UserModel, date_start: datetime, date_end: datetime, **search_kwargs) -> list[SpacedRepetitionsModel]:
        def function_filter(model) -> bool:
            result_filter: bool = model.date_repetition.timestamp() > date_start.timestamp() \
                and date_end.timestamp() > model.date_last_repetition.timestamp()
            if result_filter:
                if search_kwargs.get("title"):
                    result_filter = model.title.__contains__(
                        search_kwargs.get("title"))
                elif search_kwargs.get("slug"):
                    result_filter = model.slug == search_kwargs.get("slug")

            return result_filter

        all_user_repetiotions: list[SpacedRepetitionsModel] = await cls.get_user_repetitions(cls, current_user)
        return replacement_filter(function_filter, all_user_repetiotions)
