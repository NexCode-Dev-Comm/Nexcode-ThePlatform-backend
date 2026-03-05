from fastapi import FastAPI

app = FastAPI()

projects = [
    {"id": 1, "name": "Nexcode Platform", "status": "active"},
    {"id": 2, "name": "backend API", "status": "active"},
]

@app.get("/api/projects")
async def get_all_projects():
    return projects

