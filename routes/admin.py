from fastapi import APIRouter

app = APIRouter(prefix="/admin", tags=["admin"])

@app.get("/")
async def home():
    ...