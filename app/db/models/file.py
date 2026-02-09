from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base, engine
from datetime import datetime, timezone

class UploadedFiles(Base):
    __tablename__ = "uploaded_files"

    file_id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    file_path = Column(String)
    file_name = Column(String)
    # upload_time = Column(DateTime, default=datetime.now(timezone.utc).isoformat())
    upload_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SharedFiles(Base):
    __tablename__ = "shared_files"

    id = Column(String, primary_key=True, index=True)
    file_id = Column(String, index=True)
    sender_id = Column(String)
    receiver_id = Column(String)    
    shared_time = Column(DateTime, default=datetime.now(timezone.utc).isoformat())

Base.metadata.create_all(bind=engine)