from pydantic import BaseModel
from typing import List

class Clinic(BaseModel):
    id: int
    mobile: str
    name: str
    address: str
    latitude: float
    longitude: float
    createdAt: str
    updatedAt: str

class ClinicList(BaseModel):
    message: List[Clinic]
    status: int
