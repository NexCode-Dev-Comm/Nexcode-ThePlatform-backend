from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


contributions = Table(
    "contributions",
    Base.metadata,
    Column("member_id", Integer, ForeignKey("members.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("role_name", String, default="CONTRIBUTOR")
)


class MemberModel(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    github_url = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    global_role = Column(String, default="CONTRIBUTOR")



    projects = relationship(
        "ProjectModel",
        secondary=contributions,
        back_populates="members"
    )



class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    code_name = Column(String)    
    code_content = Column(Text)
    tech_stack = Column(String)
    
    contributors_count = Column(Integer, default=0)
    image_url = Column(String, nullable=True)


    members = relationship(
        "MemberModel",
        secondary=contributions,
        back_populates="projects"
    )




