from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from app.db.database import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    # is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(bind=engine)
