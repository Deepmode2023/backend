from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from enum import Enum
import uuid

from db.models import Base
from src.spaced_repetitions.models import SpacedRepetitionsModel


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=False)
    hashed_password = Column(String, nullable=False)
    avatar_small = Column(String, nullable=True)
    avatar_big = Column(String, nullable=True)
    roles = Column(ARRAY(String), nullable=False)
    user_words = relationship("WordModel", back_populates='user',
                              cascade="all, delete-orphan")
    shared_preference = relationship(
        "SharedPreferenceModel", back_populates="user", cascade="all, delete-orphan")
    spaced_repetitions = relationship(
        SpacedRepetitionsModel, back_populates='user',
        cascade="all, delete-orphan")

    def __repr__(self):
        return f'UserModel(user_id={self.user_id}, email={self.email})'

    @property
    def is_superadmin(self) -> bool:
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return {*self.roles, PortalRole.ROLE_PORTAL_ADMIN}

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return {role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN}

    @property
    def toJson(self):
        return {
            "user_id": str(self.user_id),
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "roles": self.roles
        }
