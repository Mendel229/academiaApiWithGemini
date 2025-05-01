from sqlalchemy.orm import Session
from typing import List

from app.models.bonne_reponse import BonneReponse, BonneReponseCreate, BonneReponseDB

class BonneReponseService:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, bonne_reponse_in: BonneReponseCreate) -> BonneReponse:
        db_bonne_reponse = BonneReponseDB(**bonne_reponse_in.model_dump())
        self.db.add(db_bonne_reponse)
        self.db.commit()
        self.db.refresh(db_bonne_reponse)
        return BonneReponse.from_orm(db_bonne_reponse)

    def lire(self, id_bonne_reponse: int) -> BonneReponse | None:
        bonne_reponse = self.db.query(BonneReponseDB).filter(BonneReponseDB.id_bonne_reponse == id_bonne_reponse).first()
        if bonne_reponse:
            return BonneReponse.from_orm(bonne_reponse)
        return None

    def lire_tous(self) -> List[BonneReponse]:
        bonnes_reponses = self.db.query(BonneReponseDB).all()
        return [BonneReponse.from_orm(bonne_reponse) for bonne_reponse in bonnes_reponses]

    def mettre_a_jour(self, id_bonne_reponse: int, bonne_reponse_in: BonneReponseCreate) -> BonneReponse | None:
        db_bonne_reponse = self.db.query(BonneReponseDB).filter(BonneReponseDB.id_bonne_reponse == id_bonne_reponse).first()
        if db_bonne_reponse:
            for field, value in bonne_reponse_in.model_dump().items():
                setattr(db_bonne_reponse, field, value)
            self.db.commit()
            self.db.refresh(db_bonne_reponse)
            return BonneReponse.from_orm(db_bonne_reponse)
        return None

    def supprimer(self, id_bonne_reponse: int):
        bonne_reponse = self.db.query(BonneReponseDB).filter(BonneReponseDB.id_bonne_reponse == id_bonne_reponse).first()
        if bonne_reponse:
            self.db.delete(bonne_reponse)
            self.db.commit()