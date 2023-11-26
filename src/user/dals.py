from datetime import datetime

from utils.hasher import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from typing import Optional, Union

from utils.image import ImageCreaterModel, ReturnedImageCreaterModel, PathnameUrl
from .models import UserModel, PortalRole
from utils.user_issues import check_user_by_email_or_id_in_db, RaiseUpByUserCondition
from src.shared_preference.models import SharedPreferenceModel, ThemeColor


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user_account(self, name: str, surname: str, email: str, password: str, avatar: Optional[bytes] = None) -> UserModel:
        await check_user_by_email_or_id_in_db(email=email, raise_up_by_user_condition=RaiseUpByUserCondition.NOT_EXIST)
        new_user = UserModel(name=name, surname=surname, email=email,
                             hashed_password=Hasher.get_password_hash(password), roles=[PortalRole.ROLE_PORTAL_USER])
        shared_preference_instance = SharedPreferenceModel(
            shared_mode=False, user=new_user, theme=ThemeColor.WHITE_THEME)

        self.db_session.add_all([new_user, shared_preference_instance])
        await self.db_session.commit()
        return new_user

    async def update_user_account(self, me: UserModel, is_access: bool, image_instance: ImageCreaterModel, **kwargs) -> Union[UserModel, None]:
        email = kwargs.get('email', None) if is_access else me.email

        created_img: ReturnedImageCreaterModel = image_instance.create_image()
        if created_img.is_create:
            kwargs.update(**{"avatar_small": created_img.pathname.small,
                          "avatar_big": created_img.pathname.big, "updated_account": datetime.utcnow()})

        if email is not None:
            updated_user = await self.db_session.scalars(update(UserModel).where(UserModel.email == email).values(
                **kwargs).returning(UserModel))

            await self.db_session.commit()
            return updated_user.one_or_none()
