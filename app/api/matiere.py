# app/routers/matiere_router.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from app.services.matiere_service import MatiereService
from app.models.matiere import MatiereCreate
from app.database import get_db

router = APIRouter(prefix="/matieres", tags=["Matieres"])

def create_response(success: bool, status: int, message):
    return JSONResponse(status_code=status, content={"success": success, "status": status, "message": message})

@router.post("/")
async def creer_matiere(matiere_in: MatiereCreate, db: Session = Depends(get_db)):
    try:
        service = MatiereService(db)
        matiere = service.creer(matiere_in)
        return create_response(True, 201, jsonable_encoder(matiere))
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la création : {str(e)}")

@router.get("/")
async def lire_matieres(db: Session = Depends(get_db)):
    service = MatiereService(db)
    matieres = service.lire_tous()
    return create_response(True, 200, jsonable_encoder(matieres))

@router.get("/{id_matiere}")
async def lire_matiere(id_matiere: int, db: Session = Depends(get_db)):
    service = MatiereService(db)
    matiere = service.lire(id_matiere)
    if matiere is None:
        return create_response(False, 404, "Matière non trouvée")
    return create_response(True, 200, jsonable_encoder(matiere))

@router.put("/{id_matiere}")
async def mettre_a_jour_matiere(id_matiere: int, matiere_in: MatiereCreate, db: Session = Depends(get_db)):
    service = MatiereService(db)
    matiere = service.mettre_a_jour(id_matiere, matiere_in)
    if matiere is None:
        return create_response(False, 404, "Matière non trouvée")
    return create_response(True, 200, jsonable_encoder(matiere))

@router.delete("/{id_matiere}")
async def supprimer_matiere(id_matiere: int, db: Session = Depends(get_db)):
    try:
        service = MatiereService(db)
        service.supprimer(id_matiere)
        return create_response(True, 204, "Matière supprimée avec succès")
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la suppression : {str(e)}")
