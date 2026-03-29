from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from sqlalchemy import insert

app = FastAPI(
    title="Nexcode API",
    description="Backend API for Nexcode Community Platform.",
)


models.Base.metadata.create_all(bind=database.engine)



# members
@app.get("/api/members", response_model=List[schemas.Member])
def get_members(db: Session = Depends(database.get_db)):
    return db.query(models.MemberModel).all()


@app.post("/api/members", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(database.get_db)):
    proj_str = ",".join(map(str, member.projects))
    db_member = models.MemberModel(
        first_name=member.first_name,
        last_name=member.last_name,
        photo_url=member.photo_url,
        github_url=member.github_url,
        global_role="CONTRIBUTOR"
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



@app.get("/members/{member_id}", response_model=schemas.MemberProfile)
def get_member_profile(member_id: int, db: Session = Depends(database.get_db)):
    member = db.query(models.MemberModel).filter(models.MemberModel.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    contrib_rows = db.execute(
        models.contributions.select().where(models.contributions.c.member_id == member_id)
    ).fetchall()

    portfolio_data = []
    for row in contrib_rows:
        project = db.query(models.ProjectModel).filter(models.ProjectModel.id == row.project_id).first()
        if project:
            portfolio_data.append({
                "id": project.id,
                "title": project.title,
                "role_in_this_project": row.role_name 
            })

    return {
        "name": f"{member.first_name} {member.last_name}",
        "github_url": member.github_url,
        "photo_url": member.photo_url,
        "portfolio": portfolio_data
    }



# projects

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


@app.get("/api/projects/{project_id}", response_model=schemas.ProjectDetail)
def get_project_detail(project_id: int, db: Session = Depends(database.get_db)):
    project = db.query(models.ProjectModel).filter(models.ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    contrib_rows = db.execute(
        models.contributions.select().where(models.contributions.c.project_id == project_id)
    ).fetchall()

    contributors_data = []
    for row in contrib_rows:
        user = db.query(models.MemberModel).filter(models.MemberModel.id == row.member_id).first()
        if user:
            contributors_data.append({
                "member_id": user.id,
                "project_id": project_id,
                "role_name": row.role_name 
            })

    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "code_name": project.code_name,
        "code_content": project.code_content,
        "image_url": project.image_url,
        "contributors_count": project.contributors_count,
        "contributors": contributors_data
    }





@app.post("/api/contributions")
def add_contribution(contribution: schemas.ContributionInfo, db: Session = Depends(database.get_db)):
    member = db.query(models.MemberModel).filter(models.MemberModel.id == contribution.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    project = db.query(models.ProjectModel).filter(models.ProjectModel.id == contribution.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        new_contribution = models.contributions.insert().values(
            member_id=contribution.member_id,
            project_id=contribution.project_id,
            role_name=contribution.role_name
        )
        db.execute(new_contribution)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Contribution already exists or DB error")

    return {"message": f"Member {member.id} added to project {project.id} as {contribution.role_name}"}


