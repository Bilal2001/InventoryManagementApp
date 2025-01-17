from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from ..database import get_session
from ..schemas.master import MasterAccountType
from ..schemas.admin import Admin
from ..schemas.master_support import AccountTypeCreate, AccountTypeUpdate

app = APIRouter(prefix="/account-type", tags=["account-type"])

@app.post("")
async def create_account_type(
    account_type_data: AccountTypeCreate,
    session: Session = Depends(get_session)
):    
    user = session.exec(select(Admin).where(Admin.username==account_type_data.created_by)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Admin details don't exists")
    
    account_type = session.exec(select(MasterAccountType).where(MasterAccountType.account_type==account_type_data.account_type)).first()
    if account_type:
        raise HTTPException(status_code=401, detail="AccountType already exists")

    account_type = MasterAccountType(
        created_by=account_type_data.created_by,
        account_type=account_type_data.account_type
    )
    session.add(account_type)
    session.commit()
    session.refresh(account_type)
    return account_type


@app.put("/{account_type_id}")
def update_account_type(
    account_type_id: int,
    account_type_details: AccountTypeUpdate, 
    session: Session = Depends(get_session)
):    
    account_type = session.exec(select(MasterAccountType).where(MasterAccountType.id==account_type_id, MasterAccountType.is_active==True)).first()
    
    if not account_type:
        raise HTTPException(status_code=401, detail="AccountType id doesn't exists")
    
    _account_type = session.exec(select(MasterAccountType).where(MasterAccountType.account_type==account_type_details.updated_account_type)).first()
    
    if _account_type:
        raise HTTPException(status_code=401, detail="AccountType already exists with name")
    
    account_type.account_type = account_type_details.updated_account_type
    session.add(account_type)
    session.commit()
    session.refresh(account_type)
    return account_type


@app.delete("/{account_type_id}")
def delete_account_type(
    account_type_id: int,
    session: Session = Depends(get_session)
):    
    account_type = session.exec(select(MasterAccountType).where(MasterAccountType.id==account_type_id, MasterAccountType.is_active==True)).first()
    
    if not account_type:
        raise HTTPException(status_code=401, detail="AccountType id doesn't exist")
    
    account_type.is_active = False
    session.add(account_type)
    session.commit()
    session.refresh(account_type)
    return JSONResponse(status_code=200, content={"detail": "Successfully deleted AccountType"})

@app.get("/{account_type_id}")
def get_account_type(
    account_type_id: int,
    session: Session = Depends(get_session)
):    
    account_type = session.exec(select(MasterAccountType).where(MasterAccountType.id==account_type_id, MasterAccountType.is_active==True)).first()
    
    if not account_type:
        raise HTTPException(status_code=401, detail="AccountType id doesn't exist")

    return account_type

@app.get("")
def get_all_account_types(
    session: Session = Depends(get_session)
):
    account_types = session.exec(select(MasterAccountType).where(MasterAccountType.is_active==True)).all()
    return account_types
