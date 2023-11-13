from typing import Union, Optional
from sqlalchemy import select, or_, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from utils.security import access_decorator
from utils.params_helpers import CommonParams
from .models import WordModel
from .schema import PartOfSpeach
from core.exeptions import ExeptionsSchema as core_exeptions

from .helpers import return_words_kwarg_after_check_permission


class WordDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_words(self, commonParams: CommonParams) -> list[WordModel]:
        return await self.db_session.scalars(select(WordModel).limit(commonParams.limit).offset(commonParams.skip))

    async def get_words_by_id(self, id: int) -> Union[WordModel, None]:
        word = await self.db_session.scalars(select(WordModel).where(WordModel.id == id))
        return word.one_or_none()

    async def get_words_by_slug_or_name(self, commonParams: CommonParams, slug: Optional[str], name: Optional[str]) -> list[WordModel]:
        filter_condition = or_(
            WordModel.name.ilike(f"%{name}%") if name else False,
            WordModel.slug.ilike(f"%{slug}%") if slug else False
        )
        return await self.db_session.scalars(select(WordModel).where(filter_condition).limit(commonParams.limit).offset(commonParams.skip))

    @access_decorator
    async def create_word(self, name: str, translate: str, part_of_speach: PartOfSpeach, slug: str, example: str, synonym: list[str], image_url: Union[str, None], **kwargs) -> WordModel:
        word = WordModel(user=kwargs.get("user"), slug=str.lower(slug), name=str.lower(name), translate=str.lower(translate), synonym=synonym,
                         example=str.lower(example), part_of_speach=part_of_speach, image_url=image_url)
        self.db_session.add(word)
        await self.db_session.commit()

        return word

    @access_decorator
    async def update_word(self, id: int, name: Union[str, None], translate:  Union[str, None], part_of_speach:  Union[PartOfSpeach, None], slug:  Union[str, None], example:  Union[str, None], synonym: Union[list[str], None], image_url: Union[str, None], **kwargs) -> WordModel:
        updated_word = await self.get_words_by_id(id=id)

        if updated_word == None:
            raise core_exeptions.DontExistItemInsideDB

        is_admin = kwargs.get('is_admin') or updated_word.user_id == kwargs.get(
            'user').user_id

        updated_kwargs = return_words_kwarg_after_check_permission(access_field_not_admin=['slug', "synonym",  "example"], is_admin=is_admin, name=name,
                                                                   translate=translate, part_of_speach=part_of_speach, slug=slug, example=example, synonym=synonym, image_url=image_url)

        word = await self.db_session.scalars(update(WordModel).where(
            WordModel.id == updated_word.id).values(**updated_kwargs).returning(WordModel))

        await self.db_session.commit()

        return word.one_or_none()

    @access_decorator
    async def delete_word(self, id: int, **kwargs) -> WordModel:
        deleted_word = await self.get_words_by_id(id=id)
        if deleted_word == None:
            raise core_exeptions.DontExistItemInsideDB

        if kwargs.get('is_admin', False) or kwargs.get("user").user_id == deleted_word.user_id:
            await self.db_session.execute(
                delete(WordModel).where(WordModel.id == id))
            await self.db_session.commit()
            return deleted_word
        else:
            raise core_exeptions.YouDontHaveAccessExeptions
