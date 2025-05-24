from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.affectation_epreuve import (
    AffectationEpreuveDB,
    AffectationEpreuveCreate,
    AffectationEpreuveUpdate,
)

class AffectationEpreuveService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: AffectationEpreuveCreate) -> AffectationEpreuveDB:
        obj = AffectationEpreuveDB(**data.dict(exclude_none=True))
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list(self) -> List[AffectationEpreuveDB]:
        return self.db.query(AffectationEpreuveDB).all()

    def get(self, id_: int) -> Optional[AffectationEpreuveDB]:
        return (
            self.db
            .query(AffectationEpreuveDB)
            .filter(AffectationEpreuveDB.id_affectation_epreuve == id_)
            .first()
        )

    def update(self, id_: int, data: AffectationEpreuveUpdate) -> Optional[AffectationEpreuveDB]:
        obj = self.get(id_)
        if not obj:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id_: int) -> Optional[AffectationEpreuveDB]:
        obj = self.get(id_)
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return obj
