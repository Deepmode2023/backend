from db.models import Base
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class WordModel(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=True)
    name = Column(String, nullable=False, unique=True)
    translate = Column(String, nullable=False)
    example = Column(String, nullable=True)
    synonym = Column(ARRAY(String), nullable=True)
    part_of_speach = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    user_id = Column(UUID, ForeignKey("users.user_id"))
    user = relationship("UserModel", back_populates='words')

    @property
    def toJson(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "translate": self.translate,
            "example": self.example,
            "synonym": self.synonym,
            "part_of_speach": self.part_of_speach,
            "image_url": self.image_url
        }
