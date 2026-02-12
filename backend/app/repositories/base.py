from sqlalchemy.orm import Session
from uuid import UUID

class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get(self, id):
        # Convert UUID to bytes if needed
        if isinstance(id, UUID):
            id_bytes = id.bytes
        elif isinstance(id, bytes):
            id_bytes = id
        else:
            id_bytes = UUID(str(id)).bytes
        return self.db.get(self.model, id_bytes)
    def create(self, **kwargs):
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
