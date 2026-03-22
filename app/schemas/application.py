from pydantic import BaseModel

from app.schemas.user import UserOut
from app.schemas.job import JobOut


class ApplicationCreate(BaseModel):
    message: str


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    job_id: int
    message: str
    user: UserOut
    job: JobOut

    model_config = {"from_attributes": True}
