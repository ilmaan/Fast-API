from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float

class Post(Base):
    __tabllename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False)
    