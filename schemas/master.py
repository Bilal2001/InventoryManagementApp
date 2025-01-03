from typing import Annotated, Optional
from pydantic import EmailStr, AfterValidator, SecretStr
from sqlmodel import Field
from validators import validate_phone
from base import BaseTable, BaseUpdateTable


class Role(BaseTable, table=True):
    role_name: str = Field(unique=True, nullable=False)

class Brand(BaseTable, table=True):
    brand_name: str = Field(unique=True, nullable=False)

class SKU(BaseTable, table=True):
    name: str
    description: Optional[str] = Field(default="", max_length=500)

class Status(BaseTable, table=True):
    name: str
    description: Optional[str] = Field(default="", max_length=500)

class Warehouse(BaseUpdateTable, table=True):
    name: str
    location: Optional[str] = Field(default="")
    description: Optional[str] = Field(default="", max_length=500)

class ItemCategory(BaseUpdateTable, table=True):
    name: str
    main: bool
    parent_id: Optional[int]