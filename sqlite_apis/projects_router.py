from fastapi import APIRouter, HTTPException,status,Depends
 
import sqlite3
 
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field

from sqlite_apis.data.model import Job, Project, ProjectCreate
 
projects_router = APIRouter();

db_path = '../python-server/sqlite_apis/data/singular-db.sqlite'
 



def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@projects_router.get("/", response_model=List[Project])
async def read_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch projects
    cursor.execute("SELECT * FROM Projects")
    projects_rows = cursor.fetchall()
    
    projects = []
    for project_row in projects_rows:
        # For each project, fetch associated jobs (IDs and names)
        cursor.execute("SELECT id, name FROM Jobs WHERE project_id = ?", (project_row['id'],))
        jobs = cursor.fetchall()
        
        projects.append(Project(
            id=project_row['id'],
            name=project_row['name'],
            description=project_row['description'],
            jobs=[Job(id=job['id'], name=job['name']) for job in jobs]
        ))
    
    conn.close()
    return projects

@projects_router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Projects (name, description) VALUES (?, ?)",
                   (project.name, project.description))
    new_project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {**project.model_dump(), "id": new_project_id}



@projects_router.get("/{project_id}", response_model=Project)
async def read_project(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch the specific project
    cursor.execute("SELECT * FROM Projects WHERE id = ?", (project_id,))
    project_row = cursor.fetchone()
    
    if project_row is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Fetch associated jobs for the specific project
    cursor.execute("SELECT id, name FROM Jobs WHERE project_id = ?", (project_id,))
    jobs = cursor.fetchall()
    
    project = Project(
        id=project_row['id'],
        name=project_row['name'],
        description=project_row['description'],
        jobs=[Job(id=job['id'], name=job['name']) for job in jobs]
    )
    
    conn.close()
    return project

@projects_router.put("/{project_id}", response_model=Project)
async def update_project(project_id: int, project: ProjectCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Projects SET name = ?, description = ? WHERE id = ?",
                   (project.name, project.description, project_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    conn.commit()
    conn.close()
    return {**project.model_dump(), "id": project_id}

@projects_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Projects WHERE id = ?", (project_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    conn.commit()
    conn.close()
    return {"message": "Project deleted successfully"}