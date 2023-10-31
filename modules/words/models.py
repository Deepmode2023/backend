from db.models import Base
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Column, String, Integer, ForeignKey


class WordModel(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    synonym = Column(ARRAY(String), nullable=True)
    part_of_speach = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    user_id = Column(UUID, ForeignKey("users.user_id"))
