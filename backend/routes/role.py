from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, update

from ..auth import create_access_token, get_password_hash, verify_password
from ..database import get_session
from ..schemas.master import MasterRole
from ..schemas.admin import Admin
from ..schemas.master_support import RoleCreate, RoleUpdate

app = APIRouter(prefix="/role", tags=["role"])

@app.post("/role")
async def create_role(
    role_data: RoleCreate,
    session: Session = Depends(get_session)
):    
    user = session.exec(select(Admin).where(Admin.username==role_data.created_by)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Admin details don't exists")
    
    role = session.exec(select(MasterRole).where(MasterRole.role_name==role_data.role_name)).first()
    if role:
        raise HTTPException(status_code=401, detail="Role already exists")

    role = MasterRole(
        created_by=role_data.created_by,
        role_name=role_data.role_name
    )
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


@app.put("/role/{role_id}")
def update_role(
    role_id: int,
    role_details: RoleUpdate, 
    session: Session = Depends(get_session)
):    
    role = session.exec(select(MasterRole).where(MasterRole.id==role_id, MasterRole.is_active==True)).first()
    
    if not role:
        raise HTTPException(status_code=401, detail="Role id doesn't exists")
    
    _role = session.exec(select(MasterRole).where(MasterRole.role_name==role_details.updated_role_name)).first()
    
    if _role:
        raise HTTPException(status_code=401, detail="Role already exists with name")
    
    role.role_name = role_details.updated_role_name
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


@app.delete("/role/{role_id}")
def delete_role(
    role_id: int,
    session: Session = Depends(get_session)
):    
    role = session.exec(select(MasterRole).where(MasterRole.id==role_id, MasterRole.is_active==True)).first()
    
    if not role:
        raise HTTPException(status_code=401, detail="Role id doesn't exist")
    
    role.is_active = False
    session.add(role)
    session.commit()
    session.refresh(role)
    return JSONResponse(status_code=200, content={"detail": "Successfully deleted Role"})

@app.get("/role/{role_id}")
def get_role(
    role_id: int,
    session: Session = Depends(get_session)
):    
    role = session.exec(select(MasterRole).where(MasterRole.id==role_id, MasterRole.is_active==True)).first()
    
    if not role:
        raise HTTPException(status_code=401, detail="Role id doesn't exist")

    return role

@app.get("/role")
def get_all_roles(
    session: Session = Depends(get_session)
):
    roles = session.exec(select(MasterRole).where(MasterRole.is_active==True)).all()
    return roles
