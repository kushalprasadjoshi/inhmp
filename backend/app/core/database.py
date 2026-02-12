################ # SQLAlchemy engine, session factory, Base ###################

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid
from sqlalchemy import event

from backend.app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
@event.listens_for(engine, "before_cursor_execute")
def _handle_uuid(conn, cursor, statement, params, context, executemany):
    if params:
        for key, val in list(params.items()):
            if isinstance(val, uuid.UUID):
                params[key] = val.bytes
                
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()