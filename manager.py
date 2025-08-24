from database.config.config import get_engine
from database.models.base import Base

if __name__ == "__main__":
    Base.metadata.create_all(get_engine())
