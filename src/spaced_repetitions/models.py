from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from enum import Enum

from utils.uuid import compare_uuid
from db.models import Base


class SlugRepetitions(str, Enum):
    WORD = "WORD"
    PDF = "PDF"
    TEXT = "TEXT"


class SpacedRepetitionsModel(Base):
    __tablename__ = "spaced_repetition"

    id = Column(Integer, primary_key=True)
    slug = Column(String(20), nullable=False, default=SlugRepetitions.WORD)
    title = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey(
        "users.user_id", ondelete="CASCADE", name="fk_user_id"))
    user = relationship(
        "UserModel", back_populates='spaced_repetitions')
    count_repetition = Column(Integer, default=1)
    date_repetition = Column(DateTime(timezone=True), nullable=False)
    date_last_repetition = Column(
        DateTime(timezone=True), nullable=False)

    def __repr__(cls):
        return f"SpacedRepetiotionsModel(id={cls.id}, title={cls.title})"

    def __eq__(cls, other):
        if isinstance(other, SpacedRepetitionsModel):
            return cls.slug == other.slug \
                and cls.title == other.title \
                and compare_uuid(cls.user_id, other.user_id)
        return False

    @property
    def toJson(cls,):
        return {
            "id": cls.id,
            "title": cls.title,
            "slug": cls.slug,
            "description": cls.description,
            "user_id": cls.user_id,
            "count_repetition": cls.count_repetition,
            "date_repetition": cls.date_repetition,
            "date_last_repetition": cls.date_last_repetition
        }
