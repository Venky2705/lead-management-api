from pydantic import BaseModel


class LeadCreate(BaseModel):
    company: str
    contact_name: str
    email: str
    country: str
    status: str