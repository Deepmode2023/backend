from utils.hasher import Hasher
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel, PortalRole
from utils.user_issues import check_user_by_email_or_id_in_db, RaiseUpByUserCondition


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user_account(self, name: str, surname: str, email: str, password: str) -> UserModel:
        await check_user_by_email_or_id_in_db(email=email, raise_up_by_user_condition=RaiseUpByUserCondition.NOT_EXIST)
        new_user = UserModel(name=name, surname=surname, email=email,
                             hashed_password=Hasher.get_password_hash(password), roles=[PortalRole.ROLE_PORTAL_USER])
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user