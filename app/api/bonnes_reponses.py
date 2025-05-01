from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.models.bonne_reponse import BonneReponse, BonneReponseCreate, BonneReponseDB  # Importe les modèles
from app.services.bonne_reponse_service import BonneReponseService
from app.database import get_db

router = APIRouter(prefix="/bonnes_reponses", tags=["Bonnes Réponses"])

@router.post("/", response_model=BonneReponse, status_code=201)
async def creer_bonne_reponse(bonne_reponse_in: BonneReponseCreate, db: Session = Depends(get_db)):
    bonne_reponse_service = BonneReponseService(db)
    return bonne_reponse_service.creer(bonne_reponse_in)

@router.get("/", response_model=List[BonneReponse])
async def lire_toutes_les_bonnes_reponses(db: Session = Depends(get_db)):
    bonne_reponse_service = BonneReponseService(db)
    return bonne_reponse_service.lire_tous()

@router.get("/{id_bonne_reponse}", response_model=BonneReponse)
async def lire_bonne_reponse(id_bonne_reponse: int, db: Session = Depends(get_db)):
    bonne_reponse_service = BonneReponseService(db)
    bonne_reponse = bonne_reponse_service.lire(id_bonne_reponse)
    if bonne_reponse is None:
        raise HTTPException(status_code=404, detail="Bonne réponse non trouvée")
    return bonne_reponse

@router.put("/{id_bonne_reponse}", response_model=BonneReponse)
async def mettre_a_jour_bonne_reponse(id_bonne_reponse: int, bonne_reponse_in: BonneReponseCreate, db: Session = Depends(get_db)):
    bonne_reponse_service = BonneReponseService(db)
    bonne_reponse = bonne_reponse_service.mettre_a_jour(id_bonne_reponse, bonne_reponse_in)
    if bonne_reponse is None:
        raise HTTPException(status_code=404, detail="Bonne réponse non trouvée")
    return bonne_reponse

@router.delete("/{id_bonne_reponse}", status_code=204)
async def supprimer_bonne_reponse(id_bonne_reponse: int, db: Session = Depends(get_db)):
    bonne_reponse_service = BonneReponseService(db)
    bonne_reponse_service.supprimer(id_bonne_reponse)
    return