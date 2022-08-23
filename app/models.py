from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(200), nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    