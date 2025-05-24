from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enseignement import EnseignementCreate, EnseignementRead
from app.services.enseignement_service import (
    create_enseignement,
    get_enseignements,
    get_enseignement_by_id,
    delete_enseignement,
)
from app.utils.format_reponse import create_response

router = APIRouter(
    prefix="/enseignements",
    tags=["Enseignements"]
)

@router.post("/", response_model=EnseignementRead)
def create(enseignement: EnseignementCreate, db: Session = Depends(get_db)):
    db_ens = create_enseignement(db, enseignement)
    ens_json = jsonable_encoder(db_ens)
    return create_response(True, 200, ens_json)

@router.get("/", response_model=list[EnseignementRead])
def read_all(db: Session = Depends(get_db)):
    ens_list = get_enseignements(db)
    list_json = jsonable_encoder(ens_list)
    return create_response(True, 200, list_json)

@router.get("/{enseignement_id}", response_model=EnseignementRead)
def read_one(enseignement_id: int, db: Session = Depends(get_db)):
    ens = get_enseignement_by_id(db, enseignement_id)
    if not ens:
        raise HTTPException(status_code=404, detail="Enseignement non trouvé")
    ens_json = jsonable_encoder(ens)
    return create_response(True, 200, ens_json)

@router.delete("/{enseignement_id}")
def delete(enseignement_id: int, db: Session = Depends(get_db)):
    ens = delete_enseignement(db, enseignement_id)
    if not ens:
        raise HTTPException(status_code=404, detail="Enseignement non trouvé")
    ens_json = jsonable_encoder(ens)
    return create_response(True, 200, ens_json)
