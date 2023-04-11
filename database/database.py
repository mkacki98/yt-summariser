import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost/yt-summariser",
    echo=True,
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
