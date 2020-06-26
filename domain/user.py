from sqlalchemy import Column, Integer, String
from infra.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    access_token = Column(String(255))
    github_id = Column(Integer)
    login = Column(String(255))
