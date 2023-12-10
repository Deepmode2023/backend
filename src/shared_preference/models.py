from sqlalchemy import Column, Boolean, ForeignKey, String, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum
import uuid

from db.models import Base


class ThemeColor(str, Enum):
    WHITE_THEME = "WHITE_THEME"
    DARK_THEME = "DARK_THEME"


class SharedPreferenceModel(Base):
    __tablename__ = "shared_preference"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    theme = Column(String, nullable=False, default=ThemeColor.WHITE_THEME)
    shared_mode = Column(Boolean, nullable=False, default=False)
    user = relationship(
        "UserModel", back_populates="shared_preference")
    user_id = Column(UUID, ForeignKey(
        "users.user_id", ondelete="CASCADE"), unique=True)

    def __repr__(self):
        return f'SharedPreferenceModel(id={self.id}, user_id={self.user_id})'

    @property
    def to_json(self):
        return {
            "theme": self.theme,
            "shared_mode": self.shared_mode,
            "user_id": self.user_id
        }


ForeignKeyConstraint(
    ["user_id"], ["users.user_id"], ondelete="CASCADE"
)
