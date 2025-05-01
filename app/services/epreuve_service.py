from sqlalchemy.orm import Session
from typing import List

from app.models.epreuve import Epreuve, EpreuveCreate, EpreuveDB

class EpreuveService:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, epreuve_in: EpreuveCreate) -> Epreuve:
        db_epreuve = EpreuveDB(**epreuve_in.model_dump())
        self.db.add(db_epreuve)
        self.db.commit()
        self.db.refresh(db_epreuve)
        return Epreuve.from_orm(db_epreuve)

    def lire(self, id_epreuve: int) -> Epreuve | None:
        epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == id_epreuve).first()
        if epreuve:
            return Epreuve.from_orm(epreuve)
        return None

    def lire_tous(self) -> List[Epreuve]:
        epreuves = self.db.query(EpreuveDB).all()
        return [Epreuve.from_orm(epreuve) for epreuve in epreuves]

    def mettre_a_jour(self, id_epreuve: int, epreuve_in: EpreuveCreate) -> Epreuve | None:
        db_epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == id_epreuve).first()
        if db_epreuve:
            for field, value in epreuve_in.model_dump().items():
                setattr(db_epreuve, field, value)
            self.db.commit()
            self.db.refresh(db_epreuve)
            return Epreuve.from_orm(db_epreuve)
        return None

    def supprimer(self, id_epreuve: int):
        epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == id_epreuve).first()
        if epreuve:
            self.db.delete(epreuve)
            self.db.commit()