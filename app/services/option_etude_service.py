# app/services/option_etude_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.option_etude import OptionEtudeDB, OptionEtudeCreate, OptionEtudeRead


class OptionEtudeService:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, option_in: OptionEtudeCreate) -> OptionEtudeRead:
        db_option = OptionEtudeDB(**option_in.dict())
        self.db.add(db_option)
        self.db.commit()
        self.db.refresh(db_option)
        return OptionEtudeRead.from_orm(db_option)

    def lire(self, id_option: int) -> Optional[OptionEtudeRead]:
        option = self.db.query(OptionEtudeDB).filter(OptionEtudeDB.id_option_etude == id_option).first()
        return OptionEtudeRead.from_orm(option) if option else None

    def lire_tous(self) -> List[OptionEtudeRead]:
        options = self.db.query(OptionEtudeDB).all()
        return [OptionEtudeRead.from_orm(o) for o in options]

    def mettre_a_jour(self, id_option: int, option_in: OptionEtudeCreate) -> Optional[OptionEtudeRead]:
        db_option = self.db.query(OptionEtudeDB).filter(OptionEtudeDB.id_option_etude == id_option).first()
        if db_option:
            for key, value in option_in.dict().items():
                setattr(db_option, key, value)
            self.db.commit()
            self.db.refresh(db_option)
            return OptionEtudeRead.from_orm(db_option)
        return None

    def supprimer(self, id_option: int):
        option = self.db.query(OptionEtudeDB).filter(OptionEtudeDB.id_option_etude == id_option).first()
        if option:
            self.db.delete(option)
            self.db.commit()
