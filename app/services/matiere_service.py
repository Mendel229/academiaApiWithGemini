# app/services/matiere_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.matiere import MatiereDB, MatiereCreate, MatiereRead


class MatiereService:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, matiere_in: MatiereCreate) -> MatiereRead:
        db_matiere = MatiereDB(**matiere_in.dict())
        self.db.add(db_matiere)
        self.db.commit()
        self.db.refresh(db_matiere)
        return MatiereRead.from_orm(db_matiere)

    def lire(self, id_matiere: int) -> Optional[MatiereRead]:
        matiere = self.db.query(MatiereDB).filter(MatiereDB.id_matiere == id_matiere).first()
        return MatiereRead.from_orm(matiere) if matiere else None

    def lire_tous(self) -> List[MatiereRead]:
        matieres = self.db.query(MatiereDB).all()
        return [MatiereRead.from_orm(m) for m in matieres]

    def mettre_a_jour(self, id_matiere: int, matiere_in: MatiereCreate) -> Optional[MatiereRead]:
        db_matiere = self.db.query(MatiereDB).filter(MatiereDB.id_matiere == id_matiere).first()
        if db_matiere:
            for key, value in matiere_in.dict().items():
                setattr(db_matiere, key, value)
            self.db.commit()
            self.db.refresh(db_matiere)
            return MatiereRead.from_orm(db_matiere)
        return None

    def supprimer(self, id_matiere: int):
        matiere = self.db.query(MatiereDB).filter(MatiereDB.id_matiere == id_matiere).first()
        if matiere:
            self.db.delete(matiere)
            self.db.commit()
