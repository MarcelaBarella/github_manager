from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infra.database import Base

from domain.tag import Tag


class Repository(Base):
    __tablename__ = 'repository'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    repo_id = Column(Integer)
    description = Column(String(255))
    url = Column(String(255))
    tag_id = Column(Integer, ForeignKey('tag.id'))
    tags = relationship('Tag', backref='repository')