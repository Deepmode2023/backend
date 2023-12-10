from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from enum import Enum


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
    count_repetition = Column(Integer, default=0)
    date_repitition = Column(DateTime(timezone=True), nullable=False)
    date_last_repetition = Column(
        DateTime(timezone=True), nullable=False)

    def __repr__(self,):
        return f"SpacedRepetiotionsModel(id={self.id}, title={self.title})"

    @property
    def toJson(self,):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "user_id": self.user_id,
            "count_repetition": self.count_repetition,
            "date_repetition": self.date_repitition,
            "date_last_repetition": self.date_last_repetition
        }
