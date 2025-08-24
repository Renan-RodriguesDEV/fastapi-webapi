from sqlalchemy import Column, Integer, String

from database.config.config import get_engine
from database.models.base import Base


class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


# Cria as tabelas no banco de dados
Base.metadata.create_all(get_engine())
