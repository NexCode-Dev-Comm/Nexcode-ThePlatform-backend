from pydantic import BaseModel
from typing import Optional, List


# members
class MemberBase(BaseModel):
    first_name: str
    last_name: str
    photo_url: Optional[str] = None
    github_url: Optional[str] = None


class MemberCreate(MemberBase):
    pass


class Member(MemberBase):
    id: int

    class Config:
        from_attributes = True


class MemberProfile(BaseModel):
    name: str
    github_url: Optional[str] = None
    photo_url: Optional[str] = None
    portfolio: List[dict]


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



# contributions
class ContributionInfo(BaseModel):
    member_id: int
    project_id: int
    role_name: str  


class ProjectDetail(Project):
    contributors: List[ContributionInfo]

    class Config:
        from_attributes = True



