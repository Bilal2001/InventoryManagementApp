from typing import Annotated, Optional
from pydantic import EmailStr, AfterValidator, SecretStr
from sqlmodel import Field, Relationship
from .validators import validate_phone
from .base import BaseTable, BaseUpdateTable

class Diying(BaseUpdateTable, table=True):
    ...

class Stiching(BaseUpdateTable, table=True):
    ...

class Washing(BaseUpdateTable, table=True):
    ...