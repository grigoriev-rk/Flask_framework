import os
import atexit
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_USER = os.getenv('PG_USER', 'app')
PG_PASSWORD = os.getenv('PG_PASSWORD', '1234')
PG_DB = os.getenv('PG_DB', 'app_flask')
PG_HOST = os.getenv('PG_HOST', '127.0.0.1')
PG_PORT = os.getenv('PG_PORT', 5431)
PG_DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

engine = create_engine(PG_DSN)
atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Ads(Base):
    __tablename__ = 'app_flask'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)


Base.metadata.create_all()

