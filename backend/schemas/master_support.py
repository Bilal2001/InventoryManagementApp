from .validators import validate_phone
from pydantic import EmailStr, AfterValidator
from typing import Annotated, Optional
from pydantic import BaseModel


class RoleCreate(BaseModel):
    created_by: str
    role_name: str

class RoleUpdate(BaseModel):
    updated_role_name: str