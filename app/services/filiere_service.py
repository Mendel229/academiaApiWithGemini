# app/services/filiere_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.filiere import FiliereDB, FiliereCreate, FiliereRead


class FiliereService:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, filiere_in: FiliereCreate) -> FiliereRead:
        db_filiere = FiliereDB(**filiere_in.dict())
        self.db.add(db_filiere)
        self.db.commit()
        self.db.refresh(db_filiere)
        return FiliereRead.from_orm(db_filiere)

    def lire(self, id_filiere: int) -> Optional[FiliereRead]:
        filiere = self.db.query(FiliereDB).filter(FiliereDB.id_filiere == id_filiere).first()
        return FiliereRead.from_orm(filiere) if filiere else None

    def lire_tous(self) -> List[FiliereRead]:
        filieres = self.db.query(FiliereDB).all()
        return [FiliereRead.from_orm(f) for f in filieres]

    def mettre_a_jour(self, id_filiere: int, filiere_in: FiliereCreate) -> Optional[FiliereRead]:
        db_filiere = self.db.query(FiliereDB).filter(FiliereDB.id_filiere == id_filiere).first()
        if db_filiere:
            for key, value in filiere_in.dict().items():
                setattr(db_filiere, key, value)
            self.db.commit()
            self.db.refresh(db_filiere)
            return FiliereRead.from_orm(db_filiere)
        return None

    def supprimer(self, id_filiere: int):
        filiere = self.db.query(FiliereDB).filter(FiliereDB.id_filiere == id_filiere).first()
        if filiere:
            self.db.delete(filiere)
            self.db.commit()
