from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.session_examen import (
    SessionExamenDB,
    SessionExamenCreate,
    SessionExamenUpdate,
)

class SessionExamenService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SessionExamenCreate) -> SessionExamenDB:
        obj = SessionExamenDB(**data.dict(exclude_none=True))
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list(self) -> List[SessionExamenDB]:
        return self.db.query(SessionExamenDB).all()

    def get(self, id_: int) -> Optional[SessionExamenDB]:
        return (
            self.db
            .query(SessionExamenDB)
            .filter(SessionExamenDB.id_session_examen == id_)
            .first()
        )

    def update(self, id_: int, data: SessionExamenUpdate) -> Optional[SessionExamenDB]:
        obj = self.get(id_)
        if not obj:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id_: int) -> Optional[SessionExamenDB]:
        obj = self.get(id_)
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return obj