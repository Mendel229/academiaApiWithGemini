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

@router.post("/", response_model=AffectationEpreuveRead)
def create_affectation(aff: AffectationEpreuveCreate, db: Session = Depends(get_db)):
    service = AffectationEpreuveService(db)
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
