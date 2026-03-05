from pydantic import BaseModel
from typing import Optional

class Project(BaseModel):
    id: int
    name: str
    status: str

    class Config:
        from_attributes = True 
