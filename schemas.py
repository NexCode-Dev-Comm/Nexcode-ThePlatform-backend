from pydantic import BaseModel
from typing import Optional, List


# members
class MemberBase(BaseModel):
    first_name: str
    last_name: str
    photo_url: Optional[str] = None
    github_url: Optional[str] = None
    projects: List[int] = []


class MemberCreate(MemberBase):
    pass


class Member(MemberBase):
    id: int

    class Config:
        from_attributes = True




# projects
class ProjectCreate(BaseModel):
    title: str
    description: str
    code_name: str
    code_content: str
    image_url: Optional[str] = None



class Project(ProjectCreate):
    id: int
    contributors_count: int

    class Config:
        from_attributes = True

