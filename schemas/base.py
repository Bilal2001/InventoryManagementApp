from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class BaseTable(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str
    
class BaseUpdateTable(BaseTable):
    updated_at: datetime = Field(default_factory=datetime.now)