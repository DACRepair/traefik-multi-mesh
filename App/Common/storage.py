from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from App.Common.config import DB_URI

engine = create_engine(DB_URI)
base = declarative_base(bind=engine)


def session():
    return scoped_session(sessionmaker(bind=engine))
