from typing import Annotated, Optional
from pydantic import EmailStr, AfterValidator, SecretStr
from validators import validate_phone
from base import BaseUpdateTable


class Admin(BaseUpdateTable, table=True):
    username: str
    email: EmailStr
    # to get value from password -> user.password.get_secret_value()
    password: SecretStr
    phone_number: Annotated[str, AfterValidator(validate_phone)]
    role: Optional[str] = ""