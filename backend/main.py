from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import *
from sqlmodel import SQLModel
from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: Initialize resources
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Shutdown code: Cleanup resources


app = FastAPI(debug=True, lifespan=lifespan)


#* Routes
app.include_router(AdminRoute)

#* Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)