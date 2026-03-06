from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)

@app.get("/api/projects", response_model=list[schemas.Project])
def get_projects(db: Session = Depends(database.get_db)):
    projects = db.query(models.ProjectModel).all()
    return projects

