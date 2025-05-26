from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.affectation_epreuve import (
    AffectationEpreuveCreate,
    AffectationEpreuveRead,
    AffectationEpreuveUpdate,
)
from app.services.affectation_epreuve_service import AffectationEpreuveService
from app.utils.format_reponse import create_response

router = APIRouter(
    prefix="/api/exam-service/affectations",
    tags=["AffectationEpreuve"]
)

@router.get("/", response_model=list[AffectationEpreuveRead])
def list_affectations(db: Session = Depends(get_db)):
    service = AffectationEpreuveService(db)
    items = service.list()
    payload = jsonable_encoder(items)
    return create_response(True, 200, payload)

@router.get("/by-session/{session_id}", response_model=list[AffectationEpreuveRead])
def list_affectations_by_session(session_id: int, db: Session = Depends(get_db)):
    service = AffectationEpreuveService(db)
    items = service.list_by_session(session_id)
    if not items:
        return create_response(True, 200, [])
    payload = jsonable_encoder(items)
    return create_response(True, 200, payload)

@router.post("/", response_model=AffectationEpreuveRead)
def create_affectation(aff: AffectationEpreuveCreate, db: Session = Depends(get_db)):
    service = AffectationEpreuveService(db)
    
    # Validation supplémentaire pour s'assurer qu'id_epreuve est bien null à la création
    if aff.id_epreuve is not None:
        raise HTTPException(
            status_code=400,
            detail="Une nouvelle affectation ne doit pas avoir d'épreuve associée initialement"
        )
    
    obj = service.create(aff)
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)

@router.get("/{id_affectation_epreuve}", response_model=AffectationEpreuveRead)
def get_affectation(id_affectation_epreuve: int, db: Session = Depends(get_db)):
    service = AffectationEpreuveService(db)
    obj = service.get(id_affectation_epreuve)
    if not obj:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)

@router.put("/{id_affectation_epreuve}", response_model=AffectationEpreuveRead)
def update_affectation(
    id_affectation_epreuve: int,
    aff: AffectationEpreuveUpdate,
    db: Session = Depends(get_db),
):
    service = AffectationEpreuveService(db)
    obj = service.update(id_affectation_epreuve, aff)
    if not obj:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)

@router.delete("/{id_affectation_epreuve}")
def delete_affectation(id_affectation_epreuve: int, db: Session = Depends(get_db)):
    service = AffectationEpreuveService(db)
    obj = service.delete(id_affectation_epreuve)
    if not obj:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)

@router.put("/{id_affectation_epreuve}/add-epreuve", response_model=AffectationEpreuveRead)
def add_epreuve_to_affectation(
    id_affectation_epreuve: int,
    epreuve_id: int,
    db: Session = Depends(get_db)
):
    service = AffectationEpreuveService(db)
    try:
        obj = service.add_epreuve(id_affectation_epreuve, epreuve_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Affectation non trouvée")
        payload = jsonable_encoder(obj)
        return create_response(True, 200, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))