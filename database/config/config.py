import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "")


def get_engine(url=DATABASE_URL):
    return create_engine(url, echo=True)


def get_session():
    session = sessionmaker(get_engine(DATABASE_URL))()
    try:
        yield session
    except Exception as e:
        print(f"Error: {str(e)}")
        session.rollback()
        raise e
    finally:
        session.close()
