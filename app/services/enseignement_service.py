from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.enseignement import EnseignementDB, EnseignementCreate


def create_enseignement(db: Session, enseignement_data: EnseignementCreate) -> EnseignementDB:
    db_enseignement = EnseignementDB(**enseignement_data.dict())
    db.add(db_enseignement)
    db.commit()
    db.refresh(db_enseignement)
    return db_enseignement

def get_enseignements(db: Session) -> List[EnseignementDB]:
    return db.query(EnseignementDB).all()

def get_enseignement_by_id(db: Session, enseignement_id: int) -> Optional[EnseignementDB]:
    return (
        db.query(EnseignementDB)
          .filter(EnseignementDB.id_enseignement == enseignement_id)
          .first()
    )

def delete_enseignement(db: Session, enseignement_id: int) -> Optional[EnseignementDB]:
    enseignement = get_enseignement_by_id(db, enseignement_id)
    if enseignement:
        db.delete(enseignement)
        db.commit()
    return enseignement
