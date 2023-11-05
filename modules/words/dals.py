import strawberry
from typing import Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.security import get_token_hash, decode_jwt_token
from utils.params_helpers import CommonParams
from utils.user_issues import check_user_by_email_or_id_in_db
from .models import WordModel
from .schema import PartOfSpeach, Word


class WordDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_words(self, commonParams: CommonParams) -> list[WordModel]:
        return await self.db_session.scalars(select(WordModel).limit(commonParams.limit).offset(commonParams.skip))

    async def create_word(self, token_raw: Union[str, None], name: str, translate: str, part_of_speach: PartOfSpeach, slug: str, example: str, synonym: list[str], image_url: Union[str, None]) -> WordModel:
        token = get_token_hash(token_raw=token_raw)
        decode_user = decode_jwt_token(token=token)
        user_id = decode_user.get(
            "user", {'user': {"user_id": None}}).get('user_id')
        user = await check_user_by_email_or_id_in_db(
            db_session=self.db_session, user_id=user_id)
        word = WordModel(user=user, slug=str.lower(slug), name=str.lower(name), translate=str.lower(translate), synonym=synonym,
                         example=str.lower(example), part_of_speach=part_of_speach, image_url=image_url)
        self.db_session.add(word)
        await self.db_session.commit()

        return word
