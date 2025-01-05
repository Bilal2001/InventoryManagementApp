from typing import Annotated, Optional
from pydantic import EmailStr, AfterValidator
from .validators import validate_phone
from .base import BaseUpdateTable
from pydantic import BaseModel
from sqlmodel import Field


class Admin(BaseUpdateTable, table=True):
    username: str = Field(unique=True)
    email: EmailStr
    # to get value from password -> user.password.get_secret_value()
    hashed_password: str
    phone_number: str
    role: Optional[str] = ""

class RegisterAdmin(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: Annotated[str, AfterValidator(validate_phone)]

class LoginAdmin(BaseModel):
    username: str
    password: str