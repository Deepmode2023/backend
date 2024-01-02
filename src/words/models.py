from db.models import Base
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .exeptions import NotFieldExist
from db.models import Base


class WordModel(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=True)
    slang = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    translate = Column(String, nullable=False)
    example = Column(String, nullable=True)
    synonym = Column(ARRAY(String), nullable=True)
    part_of_speach = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    user_id = Column(UUID, ForeignKey(
        "users.user_id", ondelete="CASCADE", name="fk_user_id"))
    user = relationship("UserModel", back_populates='user_words')

    def __repr__(cls):
        return f'WordModel(id={cls.id}, name={cls.name})'

    @property
    def toJson(cls):
        return {
            "id": cls.id,
            "name": cls.name,
            "slug": cls.slug,
            "translate": cls.translate,
            "example": cls.example,
            "synonym": cls.synonym,
            "part_of_speach": cls.part_of_speach,
            "image_url": cls.image_url
        }

    def __getitem__(cls, item):
        word = cls.toJson.get(item, None)
        if word == None:
            raise NotFieldExist
        return word
