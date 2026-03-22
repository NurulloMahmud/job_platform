from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(BaseModel):
    name: str


class CompanyOut(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = {"from_attributes": True}
