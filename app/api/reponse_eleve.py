from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.models.reponse_eleve import ReponseEleveDB, ReponseEleveCreate, ReponseEleve
from app.services.reponse_eleve_service import ReponseEleveService
from app.database import get_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.format_reponse import create_response

router = APIRouter(prefix="/reponses", tags=["Reponses Eleves"])

@router.post("/", status_code=201)
async def creer_reponse_eleve(reponse_in: ReponseEleveCreate, db: Session = Depends(get_db)):
    reponse_service = ReponseEleveService(db)
    reponse = reponse_service.enregistrer_reponse_eleve(reponse_in)
    reponse_json = jsonable_encoder(reponse)  # <-- encodage JSON
    return create_response(True, 201, reponse_json)

@router.get("/{id_reponse}")
async def lire_reponse_eleve(id_reponse: int, db: Session = Depends(get_db)):
    reponse_service = ReponseEleveService(db)
    reponse = reponse_service.lire(id_reponse)
    if reponse is None:
        return create_response(False, 404, "Réponse de l'élève non trouvée")
    reponse_json = jsonable_encoder(reponse)  # <-- encodage JSON
    return create_response(True, 200, reponse_json)

@router.get("/")
async def lire_toutes_les_reponses_eleves(db: Session = Depends(get_db)):
    reponse_service = ReponseEleveService(db)
    reponses = reponse_service.lire_tous()
    reponses_json = jsonable_encoder(reponses)  # <-- encodage JSON
    return create_response(True, 200, reponses_json)

@router.put("/{id_reponse}")
async def mettre_a_jour_reponse_eleve(id_reponse: int, reponse_in: ReponseEleveCreate, db: Session = Depends(get_db)):
    reponse_service = ReponseEleveService(db)
    reponse = reponse_service.mettre_a_jour(id_reponse, reponse_in)
    if reponse is None:
        return create_response(False, 404, "Réponse de l'élève non trouvée")
    reponse_json = jsonable_encoder(reponse)  # <-- encodage JSON
    return create_response(True, 200, reponse_json)

@router.delete("/{id_reponse}")
async def supprimer_reponse_eleve(id_reponse: int, db: Session = Depends(get_db)):
    reponse_service = ReponseEleveService(db)
    reponse = reponse_service.supprimer(id_reponse)
    if not reponse:
        return create_response(False, 404, "Réponse de l'élève non trouvée")
    return create_response(True, 204, "Réponse de l'élève supprimée")
