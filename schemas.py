from pydantic import BaseModel
from typing import List, Optional

class Project(BaseModel):
    id: int
    title: str        
    description: str
    contributors_count: int 
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

