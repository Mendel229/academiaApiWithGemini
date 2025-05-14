from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
# from app.security import get_current_user # Si tu avais un système d'authentification
from app.models.epreuve import Epreuve, EpreuveCreate, EpreuveDB  # Importe Epreuve (Pydantic) et EpreuveDB (SQLAlchemy)
from app.services.epreuve_service import EpreuveService
from app.database import get_db
# from app.models.user import User # Si tu avais un modèle User

router = APIRouter(prefix="/epreuves", tags=["Epreuves"])

@router.post("/", response_model=Epreuve, status_code=201)
async def creer_epreuve(
    epreuve_in: EpreuveCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user) # Si tu avais l'authentification
):
    """
    Crée une nouvelle épreuve, associée à l'utilisateur actuellement authentifié (professeur).
    """
    epreuve_service = EpreuveService(db)
    # epreuve_in.id_professeur = current_user.id # Si tu avais l'authentification
    # Pour l'instant, on suppose que l'id_professeur est fourni dans le schéma EpreuveCreate
    return epreuve_service.creer(epreuve_in)

@router.get("/", response_model=List[Epreuve])
async def lire_toutes_les_epreuves(db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    return epreuve_service.lire_tous()

@router.get("/{id_epreuve}", response_model=Epreuve)
async def lire_epreuve(id_epreuve: int, db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    epreuve = epreuve_service.lire(id_epreuve)
    if epreuve is None:
        raise HTTPException(status_code=404, detail="Épreuve non trouvée")
    return epreuve

@router.put("/{id_epreuve}", response_model=Epreuve)
async def mettre_a_jour_epreuve(id_epreuve: int, epreuve_in: EpreuveCreate, db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    epreuve = epreuve_service.mettre_a_jour(id_epreuve, epreuve_in)
    if epreuve is None:
        raise HTTPException(status_code=404, detail="Épreuve non trouvée")
    return epreuve

@router.delete("/{id_epreuve}", status_code=204)
async def supprimer_epreuve(id_epreuve: int, db: Session = Depends(get_db)):
    epreuve_service = EpreuveService(db)
    epreuve_service.supprimer(id_epreuve)
    return