from sqlalchemy.orm import Session
from sqlalchemy import update
from uuid import UUID

class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get(self, id: UUID):
        return self.db.get(self.model, id)

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance