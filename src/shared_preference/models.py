from sqlalchemy import Column, Boolean, ForeignKey, String
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
    user_id = Column(UUID, ForeignKey("users.user_id"))
    user = relationship("UserModel", back_populates='words')

    def __repr__(self):
        return f'SharedPreferenceModel(id={self.id}, name={self.name})'
