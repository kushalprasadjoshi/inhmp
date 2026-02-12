import sys
import os

# Add the root directory of the project to the PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.database import engine, Base
from app.core.config import settings

# ✅ 1. FIRST – Import ALL models so SQLAlchemy knows about them
from app.models import hospital, user, patient, visit, consent, emergency_log, audit_log
# (You don't need to assign them, just import)

# ✅ 2. THEN – Create tables (this will now see all imported models)
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully (if they didn't exist).")

# ✅ 3. Import routers AFTER tables are created (optional, but safe)
from app.routers import auth, hospitals
from app.routers import patients
from app.routers import visits  # Import visit router after tables are created
from app.routers import consent
from app.routers import emergency
from app.routers import audit
from app.routers import analytics  # Import analytics router
from app.routers import ml  # Import ML router

app = FastAPI(title="INHMP API")

# Mount static frontend files
static_path = Path(__file__).parent.parent.parent / "frontend"
app.mount("/pages", StaticFiles(directory=static_path / "pages"), name="pages")
app.mount("/static", StaticFiles(directory=static_path / "assets"), name="assets")

# Include routers
app.include_router(auth.router)
app.include_router(hospitals.router)
app.include_router(patients.router)
app.include_router(visits.router)  # Include visit router
app.include_router(consent.router)
app.include_router(emergency.router)
app.include_router(audit.router)
app.include_router(analytics.router)  # Include analytics router
app.include_router(ml.router)  # Include ML router

@app.get("/")
async def read_root():
    from fastapi.responses import FileResponse
    return FileResponse(static_path / "pages/index.html")