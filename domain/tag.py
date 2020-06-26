from sqlalchemy import Column, String, Integer
from infra.database import Base

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = description = Column(String(50))