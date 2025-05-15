from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder 

from app.models.epreuve import Epreuve, EpreuveCreate
from app.services.epreuve_service import EpreuveService
from app.database import get_db
from app.utils.format_reponse import create_response

router = APIRouter(prefix="/epreuves", tags=["Epreuves"])

@router.post("/")
async def creer_epreuve(
    epreuve_in: EpreuveCreate,
    db: Session = Depends(get_db),
):
    epreuve_service = EpreuveService(db)
    epreuve = epreuve_service.creer(epreuve_in)
    # Si tu veux renvoyer l'objet créé, tu pourrais encoder :
    # epreuve_json = jsonable_encoder(epreuve)
    # return create_response(True, 201, epreuve_json)
    # Sinon, pas de modification ici car tu renvoies juste un message
    return create_response(True, 201, "Épreuve créée avec succès")

@router.get("/")
async def lire_toutes_les_epreuves(db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    epreuves = epreuve_service.lire_tous()
    epreuves_json = jsonable_encoder(epreuves)  # encode les objets complexes
    return create_response(True, 200, epreuves_json)

@router.get("/{id_epreuve}")
async def lire_epreuve(id_epreuve: int, db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    epreuve = epreuve_service.lire(id_epreuve)
    if epreuve is None:
        raise HTTPException(status_code=404, detail="Épreuve non trouvée")
    epreuve_json = jsonable_encoder(epreuve)  # encode l'objet complexe
    return create_response(True, 200, epreuve_json)

@router.put("/{id_epreuve}")
async def mettre_a_jour_epreuve(id_epreuve: int, epreuve_in: EpreuveCreate, db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    epreuve = epreuve_service.mettre_a_jour(id_epreuve, epreuve_in)
    if epreuve is None:
        raise HTTPException(status_code=404, detail="Épreuve non trouvée")
    return create_response(True, 200, "Épreuve mise à jour avec succès")

@router.delete("/{id_epreuve}")
async def supprimer_epreuve(id_epreuve: int, db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    success = epreuve_service.supprimer(id_epreuve)
    if not success:
        raise HTTPException(status_code=404, detail="Épreuve non trouvée")
    return create_response(True, 204, "Épreuve supprimée avec succès")
