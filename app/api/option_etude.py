# app/routers/option_etude_router.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from app.services.option_etude_service import OptionEtudeService
from app.models.option_etude import OptionEtudeCreate
from app.database import get_db

router = APIRouter(prefix="/options", tags=["Options d'Étude"])

def create_response(success: bool, status: int, message):
    return JSONResponse(status_code=status, content={"success": success, "status": status, "message": message})

@router.post("/")
async def creer_option(option_in: OptionEtudeCreate, db: Session = Depends(get_db)):
    try:
        service = OptionEtudeService(db)
        option = service.creer(option_in)
        return create_response(True, 201, jsonable_encoder(option))
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la création : {str(e)}")

@router.get("/")
async def lire_options(db: Session = Depends(get_db)):
    service = OptionEtudeService(db)
    options = service.lire_tous()
    return create_response(True, 200, jsonable_encoder(options))

@router.get("/{id_option}")
async def lire_option(id_option: int, db: Session = Depends(get_db)):
    service = OptionEtudeService(db)
    option = service.lire(id_option)
    if option is None:
        return create_response(False, 404, "Option non trouvée")
    return create_response(True, 200, jsonable_encoder(option))

@router.put("/{id_option}")
async def mettre_a_jour_option(id_option: int, option_in: OptionEtudeCreate, db: Session = Depends(get_db)):
    service = OptionEtudeService(db)
    option = service.mettre_a_jour(id_option, option_in)
    if option is None:
        return create_response(False, 404, "Option non trouvée")
    return create_response(True, 200, jsonable_encoder(option))

@router.delete("/{id_option}")
async def supprimer_option(id_option: int, db: Session = Depends(get_db)):
    try:
        service = OptionEtudeService(db)
        service.supprimer(id_option)
        return create_response(True, 204, "Option supprimée avec succès")
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la suppression : {str(e)}")
