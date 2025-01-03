from fastapi import FastAPI
from routes import *

app = FastAPI(debug=True)


#* Routes
app.include_router(AdminRoute)