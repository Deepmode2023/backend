from typing import Union, Optional
from sqlalchemy import select, or_, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from utils.security import access_decorator
from utils.params_helpers import CommonParams
from .models import WordModel
from .schema import PartOfSpeach
from uuid import UUID
from core.exeptions import schema as core_exeptions

from .helpers import return_words_kwarg_after_check_permission
from src.user.models import UserModel

from db.call import scalars_fetch_one_or_none, add_fetch_one_item


class WordDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_words(self, commonParams: CommonParams) -> list[WordModel]:
        return await self.db_session.scalars(select(WordModel).limit(commonParams.limmit).offset(commonParams.skip))

    async def get_words_by_id(self, id: int) -> Union[WordModel, None]:
        return await scalars_fetch_one_or_none(stmp=select(WordModel).where(WordModel.id == id))

    async def get_words_by_slug_or_name(self, commonParams: CommonParams, slug: Optional[str], name: Optional[str]) -> list[WordModel]:
        filter_condition = or_(
            WordModel.name.ilike(f"%{name}%") if name else False,
            WordModel.slug.ilike(f"%{slug}%") if slug else False
        )
        return await self.db_session.scalars(select(WordModel).where(filter_condition).limit(commonParams.limmit).offset(commonParams.skip))

    async def create_word(self, current_user: UserModel, **words_kwargs) -> WordModel:
        print(words_kwargs)
        try:
            smtp = insert(WordModel).values(user_id=UUID(
                current_user.user_id), **words_kwargs).returning(WordModel)
            return await add_fetch_one_item(smtp)
        except Exception:
            raise core_exeptions.AlreadyExistInDB

    @access_decorator
    async def update_word(self, id: int, slang: str, name: Union[str, None], translate:  Union[str, None], part_of_speach:  Union[PartOfSpeach, None], slug:  Union[str, None], example:  Union[str, None], synonym: Union[list[str], None], image_url: Union[str, None], **kwargs) -> WordModel:
        updated_word = await self.get_words_by_id(id=id)

        if updated_word == None:
            raise core_exeptions.DontExistItemInsideDB

        is_admin = kwargs.get('is_admin') or updated_word.user_id == kwargs.get(
            'user').user_id

        updated_kwargs = return_words_kwarg_after_check_permission(access_field_not_admin=['slug', "synonym",  "example"], is_admin=is_admin, name=name,
                                                                   translate=translate, part_of_speach=part_of_speach, slug=slug, example=example, synonym=synonym, image_url=image_url, slang=slang)

        word = await self.db_session.scalars(update(WordModel).where(
            WordModel.id == updated_word.id).values(**updated_kwargs).returning(WordModel))

        await self.db_session.commit()

        return word.one_or_none()

    @access_decorator
    async def delete_word(self, id: int, **kwargs) -> WordModel:
        deleted_word = await self.get_words_by_id(id=id)
        if deleted_word == None:
            raise core_exeptions.DontExistItemInsideDB

        if kwargs.get('is_admin', False) or str(kwargs.get("user", "").user_id) == str(deleted_word.user_id):
            await self.db_session.execute(
                delete(WordModel).where(WordModel.id == id))
            await self.db_session.commit()
            return deleted_word
        else:
            raise core_exeptions.YouDontHaveAccessExeptions
