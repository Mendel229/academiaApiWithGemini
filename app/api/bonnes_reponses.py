from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.bonne_reponse import BonneReponseCreate
from app.services.bonne_reponse_service import BonneReponseService
from app.database import get_db
from app.utils.format_reponse import create_response

router = APIRouter(prefix="/bonnes_reponses", tags=["Bonnes Réponses"])

@router.post("/", status_code=201)
async def creer_bonne_reponse(bonne_reponse_in: BonneReponseCreate, db: Session = Depends(get_db)):
    service = BonneReponseService(db)
    bonne_reponse = service.creer(bonne_reponse_in)
    data = jsonable_encoder({"bonne_reponse": bonne_reponse})
    return create_response(True, 201, data)

@router.get("/")
async def lire_toutes_les_bonnes_reponses(db: Session = Depends(get_db)):
    service = BonneReponseService(db)
    bonnes_reponses = service.lire_tous()
    data = jsonable_encoder({"bonnes_reponses": bonnes_reponses})
    return create_response(True, 200, data)

@router.get("/{id_bonne_reponse}")
async def lire_bonne_reponse(id_bonne_reponse: int, db: Session = Depends(get_db)):
    service = BonneReponseService(db)
    bonne_reponse = service.lire(id_bonne_reponse)
    if bonne_reponse is None:
        return create_response(False, 404, "Bonne réponse non trouvée")
    data = jsonable_encoder({"bonne_reponse": bonne_reponse})
    return create_response(True, 200, data)

@router.put("/{id_bonne_reponse}")
async def mettre_a_jour_bonne_reponse(id_bonne_reponse: int, bonne_reponse_in: BonneReponseCreate, db: Session = Depends(get_db)):
    service = BonneReponseService(db)
    bonne_reponse = service.mettre_a_jour(id_bonne_reponse, bonne_reponse_in)
    if bonne_reponse is None:
        return create_response(False, 404, "Bonne réponse non trouvée")
    data = jsonable_encoder({"bonne_reponse": bonne_reponse})
    return create_response(True, 200, data)

@router.delete("/{id_bonne_reponse}")
async def supprimer_bonne_reponse(id_bonne_reponse: int, db: Session = Depends(get_db)):
    service = BonneReponseService(db)
    success = service.supprimer(id_bonne_reponse)
    if not success:
        return create_response(False, 404, "Bonne réponse non trouvée ou déjà supprimée")
    return create_response(True, 200, "Bonne réponse supprimée avec succès")
