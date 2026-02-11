import sys
import os

# Add the root directory of the project to the PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.core.database import engine, Base
from backend.app.routers import auth

app = FastAPI(title="INHMP API")

# Create tables 
Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(auth.router)

# Mount static files (frontend)
static_path = Path(__file__).parent.parent.parent / "frontend"
app.mount("/pages", StaticFiles(directory=static_path / "pages"), name="pages")
app.mount("/static", StaticFiles(directory=static_path / "assets"), name="assets")

@app.get("/")
async def read_root():
    from fastapi.responses import FileResponse
    return FileResponse(static_path / "pages/index.html")