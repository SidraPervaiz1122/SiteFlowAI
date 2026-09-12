from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.models.project import Project
from backend.schemas.project import ProjectResponse, ProjectProgressSummary
from backend.services.boq.boq_service import get_project_progress_summary
from backend.app.dependencies import get_current_user
from backend.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/current", response_model=ProjectResponse)
def get_current_project(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == 1).first()
    if not project:
        raise HTTPException(status_code=404, detail="Current project not found")
    return ProjectResponse.model_validate(project)

@router.get("/progress", response_model=ProjectProgressSummary)
def get_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_project_progress_summary(db, project_id=1)
