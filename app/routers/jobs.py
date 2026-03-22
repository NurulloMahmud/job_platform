from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.company import Company
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate, JobOut, JobUpdate

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=List[JobOut])
def list_jobs(company_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Job)
    if company_id is not None:
        query = query.filter(Job.company_id == company_id)
    return query.all()


@router.post("/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(
        Company.id == job_in.company_id,
        Company.owner_id == current_user.id,
    ).first()
    if not company:
        raise HTTPException(status_code=403, detail="You don't own this company or it doesn't exist")
    job = Job(
        title=job_in.title,
        position=job_in.position,
        salary=job_in.salary,
        company_id=job_in.company_id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int,
    job_in: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    company = db.query(Company).filter(
        Company.id == job.company_id,
        Company.owner_id == current_user.id,
    ).first()
    if not company:
        raise HTTPException(status_code=403, detail="Not authorized")
    if job_in.title is not None:
        job.title = job_in.title
    if job_in.position is not None:
        job.position = job_in.position
    if job_in.salary is not None:
        job.salary = job_in.salary
    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    company = db.query(Company).filter(
        Company.id == job.company_id,
        Company.owner_id == current_user.id,
    ).first()
    if not company:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(job)
    db.commit()
