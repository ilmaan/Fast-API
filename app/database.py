import imp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/fast-api' 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
 
 # DEPENDENCY INJECTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
