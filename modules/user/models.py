from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from enum import Enum
import uuid


from db.models import Base


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
    roles = Column(ARRAY(String), nullable=False)
    words = relationship("words", back_populates="words")

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
