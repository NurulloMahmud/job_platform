from typing import Optional

from pydantic import BaseModel

from app.schemas.company import CompanyOut


class JobCreate(BaseModel):
    title: str
    position: str
    salary: float
    company_id: int


class JobUpdate(BaseModel):
    title: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None


class JobOut(BaseModel):
    id: int
    title: str
    position: str
    salary: float
    company_id: int
    company: CompanyOut

    model_config = {"from_attributes": True}
