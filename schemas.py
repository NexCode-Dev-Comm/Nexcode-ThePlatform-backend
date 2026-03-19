from pydantic import BaseModel
from typing import Optional



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

