from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.application import Application
from app.models.job import Job
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationOut

router = APIRouter(tags=["Applications"])


@router.post("/jobs/{job_id}/apply", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def apply_for_job(
    job_id: int,
    application_in: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not db.query(Job).filter(Job.id == job_id).first():
        raise HTTPException(status_code=404, detail="Job not found")
    if db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.job_id == job_id,
    ).first():
        raise HTTPException(status_code=400, detail="Already applied for this job")
    application = Application(
        user_id=current_user.id,
        job_id=job_id,
        message=application_in.message,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/my-applications", response_model=List[ApplicationOut])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Application).filter(Application.user_id == current_user.id).all()
