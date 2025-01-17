from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, update

from ..auth import create_access_token, get_password_hash, verify_password
from ..database import get_session
from ..schemas.master import MasterBrand
from ..schemas.admin import Admin
from ..schemas.master_support import BrandCreate, BrandUpdate

app = APIRouter(prefix="/brand", tags=["brand"])

@app.post("")
async def create_brand(
    brand_data: BrandCreate,
    session: Session = Depends(get_session)
):    
    user = session.exec(select(Admin).where(Admin.username==brand_data.created_by)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Admin details don't exists")
    
    brand = session.exec(select(MasterBrand).where(MasterBrand.brand_name==brand_data.brand_name)).first()
    if brand:
        raise HTTPException(status_code=401, detail="Brand already exists")

    brand = MasterBrand(
        created_by=brand_data.created_by,
        brand_name=brand_data.brand_name
    )
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


@app.put("/{brand_id}")
def update_brand(
    brand_id: int,
    brand_details: BrandUpdate, 
    session: Session = Depends(get_session)
):    
    brand = session.exec(select(MasterBrand).where(MasterBrand.id==brand_id, MasterBrand.is_active==True)).first()
    
    if not brand:
        raise HTTPException(status_code=401, detail="Brand id doesn't exists")
    
    _brand = session.exec(select(MasterBrand).where(MasterBrand.brand_name==brand_details.updated_brand_name)).first()
    
    if _brand:
        raise HTTPException(status_code=401, detail="Brand already exists with name")
    
    brand.brand_name = brand_details.updated_brand_name
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


@app.delete("/{brand_id}")
def delete_brand(
    brand_id: int,
    session: Session = Depends(get_session)
):    
    brand = session.exec(select(MasterBrand).where(MasterBrand.id==brand_id, MasterBrand.is_active==True)).first()
    
    if not brand:
        raise HTTPException(status_code=401, detail="Brand id doesn't exist")
    
    brand.is_active = False
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return JSONResponse(status_code=200, content={"detail": "Successfully deleted Brand"})

@app.get("/{brand_id}")
def get_brand(
    brand_id: int,
    session: Session = Depends(get_session)
):    
    brand = session.exec(select(MasterBrand).where(MasterBrand.id==brand_id, MasterBrand.is_active==True)).first()
    
    if not brand:
        raise HTTPException(status_code=401, detail="Brand id doesn't exist")

    return brand

@app.get("")
def get_all_brands(
    session: Session = Depends(get_session)
):
    brands = session.exec(select(MasterBrand).where(MasterBrand.is_active==True)).all()
    return brands
