from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import and_

from app.models.affectation_epreuve import (
    AffectationEpreuveDB,
    AffectationEpreuveCreate,
    AffectationEpreuveUpdate,
)

class AffectationEpreuveService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: AffectationEpreuveCreate) -> AffectationEpreuveDB:
        # Exclure explicitement id_epreuve si null et s'assurer du statut par défaut
        create_data = data.dict(exclude_none=True)
        
        # Si id_epreuve est explicitement null, on ne l'inclut pas
        if 'id_epreuve' in create_data and create_data['id_epreuve'] is None:
            del create_data['id_epreuve']
        
        # Assigner le statut par défaut si non fourni
        if 'statut_affectation' not in create_data:
            create_data['statut_affectation'] = "assignee"
        
        obj = AffectationEpreuveDB(**create_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list(self) -> List[AffectationEpreuveDB]:
        return self.db.query(AffectationEpreuveDB).all()

    def list_by_session(self, session_id: int) -> List[AffectationEpreuveDB]:
        return (
            self.db.query(AffectationEpreuveDB)
            .filter(AffectationEpreuveDB.id_session_examen == session_id)
            .all()
        )

    def get(self, id_: int) -> Optional[AffectationEpreuveDB]:
        return (
            self.db.query(AffectationEpreuveDB)
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
    
    # Dans AffectationEpreuveService
def add_epreuve(self, affectation_id: int, epreuve_id: int) -> Optional[AffectationEpreuveDB]:
    obj = self.get(affectation_id)
    if not obj:
        return None
    
    if obj.id_epreuve is not None:
        raise ValueError("Une épreuve est déjà associée à cette affectation")
    
    obj.id_epreuve = epreuve_id
    self.db.commit()
    self.db.refresh(obj)
    return obj