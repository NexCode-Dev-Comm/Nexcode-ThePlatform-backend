from sqlalchemy import Column, Integer, String
from database import Base

class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    contributors_count = Column(Integer, default=0)
    image_url = Column(String, nullable=True)