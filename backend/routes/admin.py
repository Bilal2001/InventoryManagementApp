from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import create_access_token, get_password_hash, verify_password
from ..database import get_session
from ..schemas.admin import Admin, RegisterAdmin, LoginAdmin

app = APIRouter(prefix="/admin", tags=["admin"])

@app.post("/register")
async def home(admin_data: RegisterAdmin,
               session: Session = Depends(get_session)):
    
    user = session.exec(select(Admin).where(Admin.username==admin_data.username)).first()
    if user:
        raise HTTPException(status_code=401, detail="Admin details already exists")

    hashed_password = get_password_hash(admin_data.password)
    user = Admin(
        username=admin_data.username,
        hashed_password=hashed_password,
        email=admin_data.email,
        phone_number=admin_data.phone,
        role="Admin"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/login")
def login(
    login_details: LoginAdmin, 
    session: Session = Depends(get_session)):
    user = session.exec(select(Admin).where(Admin.username==login_details.username)).first()
    
    if not user or not verify_password(login_details.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}