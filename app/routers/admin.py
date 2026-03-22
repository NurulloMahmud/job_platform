from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.application import Application
from app.models.company import Company
from app.models.job import Job
from app.models.user import User
from app.schemas.application import ApplicationOut

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/applications", response_model=List[ApplicationOut])
def get_vacancy_applicants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all applications for vacancies belonging to the current user's companies."""
    company_ids = [
        c.id for c in db.query(Company).filter(Company.owner_id == current_user.id).all()
    ]
    if not company_ids:
        return []
    job_ids = [
        j.id for j in db.query(Job).filter(Job.company_id.in_(company_ids)).all()
    ]
    if not job_ids:
        return []
    return db.query(Application).filter(Application.job_id.in_(job_ids)).all()
