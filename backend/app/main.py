from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .core.database import engine, Base

app = FastAPI(title="INHMP API")

# Create tables (only for hackathon - in production use Alembic)
Base.metadata.create_all(bind=engine)

# Mount static files (frontend)
static_path = Path(__file__).parent.parent.parent / "frontend"
app.mount("/pages", StaticFiles(directory=static_path / "pages"), name="pages")
app.mount("/static", StaticFiles(directory=static_path / "assets"), name="assets")

@app.get("/")
async def read_root():
    from fastapi.responses import FileResponse
    return FileResponse(static_path / "pages/index.html")