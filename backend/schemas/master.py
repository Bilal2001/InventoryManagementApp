from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field
from .base import BaseUpdateTable

class MasterRole(BaseUpdateTable, table=True):
    role_name: str = Field(unique=True, nullable=False)

class MasterUnit(BaseUpdateTable, table=True):
    unit_name: str = Field(unique=True, nullable=False)
    main: bool
    parent_id: Optional[int] = Field(foreign_key="masterunit.id")

class MasterBrand(BaseUpdateTable, table=True):
    brand_name: str = Field(unique=True, nullable=False)

class MasterSKU(BaseUpdateTable, table=True):
    name: str
    description: Optional[str] = Field(default="", max_length=500)

class MasterStatus(BaseUpdateTable, table=True):
    name: str
    description: Optional[str] = Field(default="", max_length=500)

class MasterWarehouse(BaseUpdateTable, table=True):
    name: str
    location: Optional[str] = Field(default="")
    description: Optional[str] = Field(default="", max_length=500)

class MasterAccount(BaseUpdateTable, table=True):
    account_type: str = Field(nullable=False)

class MasterAccountDetails(BaseUpdateTable, table=True):
    account_id: int = Field(nullable=False, foreign_key="masteraccount.id")
    name: str
    phone: str
    contact_person: Optional[str] = Field(default="")
    email: Optional[EmailStr] = Field(default="")
    address: Optional[str] = Field(default="", max_length=300)
    pincode: Optional[str] = Field(default="")
    remarks: Optional[str] = Field(default="", max_length=500)

class MasterItemCategory(BaseUpdateTable, table=True):
    name: str
    main: bool
    parent_id: Optional[int] = Field(nullable=False, foreign_key="masteritemcategory.id")

class MasterItem(BaseUpdateTable, table=True):
    name: str
    item_category_id: int = Field(nullable=False, foreign_key="masteritemcategory.id")
    brand_id: int = Field(nullable=False, foreign_key="masterbrand.id")
    unit_id: int = Field(nullable=False, foreign_key="masterunit.id")
    description: Optional[str] = Field(default="", max_length=500)

class MasterItemDetails(BaseUpdateTable, table=True):
    item_id: int = Field(nullable=False, foreign_key="masteritem.id")
    critical_level_alert: bool
    critical_level_quantity: int = Field(default=None, nullable=True)
    reorder_level_quantity: int = Field(default=None, nullable=True)
    reorder_level_days: int = Field(default=None, nullable=True)
    minimum_quantity: int = Field(default=None, nullable=True)
    maximum_quantity: int = Field(default=None, nullable=True)
    opening_quantity: int = Field(default=None, nullable=True)
    current_quantity: int = Field(default=None, nullable=True)

class MasterItemVendor(BaseUpdateTable, table=True):
    item_id: int = Field(nullable=False, foreign_key="masteritem.id")
    vendor_account_id: int = Field(nullable=False, foreign_key="masteraccount.id")
    purchase_price: float = Field(nullable=False)
    purchase_unit_id: int = Field(nullable=False, foreign_key="masterunit.id")
    brand_id: int = Field(nullable=False, foreign_key="masterbrand.id")
    remarks: Optional[str] = Field(default="", max_length=500)

class Purchase(BaseUpdateTable, table=True):
    ...

class PurchaseChild(BaseUpdateTable, table=True):
    ...

class PurchaseReturn(BaseUpdateTable, table=True):
    ...

class InvoiceDetail(BaseUpdateTable, table=True):
    ...

class Product(BaseUpdateTable, table=True):
    ...