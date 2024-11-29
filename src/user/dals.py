from datetime import datetime

from pydantic import EmailStr
from utils.hasher import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select
from typing import Union

from core.exeptions.schema import DontExistItemInsideDB
from utils.image import ImageCreaterModel, ReturnedImageCreaterModel, DeleterImages, PathnameUrl
from .models import UserModel, PortalRole
from db.call import scalars_fetch_one_or_none
from utils.user_issues import check_user_by_email_or_id_in_db, RaiseUpByUserCondition
from src.shared_preference.models import SharedPreferenceModel, ThemeColor


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user_account(self, image_instance: ImageCreaterModel, name: str, surname: str, email: str, password: str) -> UserModel:
        await check_user_by_email_or_id_in_db(email=email, raise_up_by_user_condition=RaiseUpByUserCondition.EXIST)

        created_image = image_instance.create_image().model_dump(
        ) if image_instance.image is not None else {}

        avatar = {"avatar_small": created_image.get("pathname").get("small") if created_image.get("is_create", False) else None,
                  "avatar_big": created_image.get("pathname").get("big") if created_image.get("is_create", False) else None}

        new_user = UserModel(name=name, surname=surname, email=email,
                             hashed_password=Hasher.get_password_hash(password), roles=[PortalRole.ROLE_PORTAL_USER], **avatar)

        shared_preference_instance = SharedPreferenceModel(
            shared_mode=False, user=new_user, theme=ThemeColor.WHITE_THEME)

        self.db_session.add_all([new_user, shared_preference_instance])
        await self.db_session.commit()
        return new_user

    async def update_user_account(self, email: EmailStr, image_instance: ImageCreaterModel, **kwargs) -> Union[UserModel, None]:
        checked_account = await scalars_fetch_one_or_none(select(UserModel).where(UserModel.email == email))

        if checked_account is not None:
            if image_instance.image is not None:
                DeleterImages.delete(pathname=PathnameUrl(
                    small=checked_account.avatar_small, big=checked_account.avatar_big) if checked_account.avatar_big and checked_account.avatar_small else None)
                created_img: ReturnedImageCreaterModel = image_instance.create_image()
                if created_img.is_create:
                    kwargs.update(**{"avatar_small": created_img.pathname.small,
                                     "avatar_big": created_img.pathname.big})

            kwargs.update(**{"updated_account": datetime.utcnow()})

            updated_user = await scalars_fetch_one_or_none(update(UserModel).where(UserModel.email == email).values(
                **kwargs).returning(UserModel), with_commit=True)
            return updated_user
        else:
            raise DontExistItemInsideDB

    async def delete_user(self, email: EmailStr) -> UserModel:
        try:
            user_model = await check_user_by_email_or_id_in_db(email=email, raise_up_by_user_condition=RaiseUpByUserCondition.NOT_EXIST)
            await self.db_session.execute(
                delete(UserModel).where(UserModel.email == email))
            await self.db_session.commit()
            return user_model
        except Exception:
            raise
