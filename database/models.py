from .database import Base
from sqlalchemy import String, DateTime, Integer, Column


class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True)
    url = Column(String, unique=True)

    created_at = Column(DateTime)
    title = Column(String)
    n_keypoints = Column(Integer)
    summary = Column(String)
