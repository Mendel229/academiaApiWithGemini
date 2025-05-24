# app/routers/filiere_router.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from app.services.filiere_service import FiliereService
from app.models.filiere import FiliereCreate
from app.database import get_db

router = APIRouter(prefix="/filieres", tags=["Filieres"])

def create_response(success: bool, status: int, message):
    return JSONResponse(status_code=status, content={"success": success, "status": status, "message": message})

@router.post("/")
async def creer_filiere(filiere_in: FiliereCreate, db: Session = Depends(get_db)):
    try:
        service = FiliereService(db)
        filiere = service.creer(filiere_in)
        return create_response(True, 201, jsonable_encoder(filiere))
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la création : {str(e)}")

@router.get("/")
async def lire_filieres(db: Session = Depends(get_db)):
    service = FiliereService(db)
    filieres = service.lire_tous()
    return create_response(True, 200, jsonable_encoder(filieres))

@router.get("/{id_filiere}")
async def lire_filiere(id_filiere: int, db: Session = Depends(get_db)):
    service = FiliereService(db)
    filiere = service.lire(id_filiere)
    if filiere is None:
        return create_response(False, 404, "Filière non trouvée")
    return create_response(True, 200, jsonable_encoder(filiere))

@router.put("/{id_filiere}")
async def mettre_a_jour_filiere(id_filiere: int, filiere_in: FiliereCreate, db: Session = Depends(get_db)):
    service = FiliereService(db)
    filiere = service.mettre_a_jour(id_filiere, filiere_in)
    if filiere is None:
        return create_response(False, 404, "Filière non trouvée")
    return create_response(True, 200, jsonable_encoder(filiere))

@router.delete("/{id_filiere}")
async def supprimer_filiere(id_filiere: int, db: Session = Depends(get_db)):
    try:
        service = FiliereService(db)
        service.supprimer(id_filiere)
        return create_response(True, 204, "Filière supprimée avec succès")
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la suppression : {str(e)}")
