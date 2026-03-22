from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database


app = FastAPI(
    title="Nexcode API",
    description="Backend API for Nexcode Community Platform.",
)


models.Base.metadata.create_all(bind=database.engine)


@app.get("/api/members", response_model=List[schemas.Member])
def get_members(db: Session = Depends(database.get_db)):
    members = db.query(models.MemberModel).all()
    for m in members:
        m.projects = [int(i) for i in m.projects_ids.split(",")] if m.projects_ids else []
    return members


@app.post("/api/members", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(database.get_db)):
    proj_str = ",".join(map(str, member.projects))
    db_member = models.MemberModel(
        first_name=member.first_name,
        last_name=member.last_name,
        photo_url=member.photo_url,
        github_url=member.github_url,
        projects_ids=proj_str
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@app.delete("/api/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(database.get_db)):
    member = db.query(models.MemberModel).filter(models.MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
    return {"message": f"Member {member_id} deleted"}







@app.get("/api/projects", response_model=list[schemas.Project])
def get_projects(db: Session = Depends(database.get_db)):
    projects = db.query(models.ProjectModel).all()
    return projects



@app.post("/api/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    db_project = models.ProjectModel(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(database.get_db)):
    project = db.query(models.ProjectModel).filter(models.ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": f"Project {project_id} deleted"}


