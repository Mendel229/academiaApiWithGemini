from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.models.reponse_eleve import ReponseEleveDB, ReponseEleveCreate, ReponseEleve
from app.services.reponse_eleve_service import ReponseEleveService
from app.database import get_db

router = APIRouter(prefix="/reponses", tags=["Reponses Eleves"])

@router.post("/", response_model=ReponseEleve, status_code=201)
async def creer_reponse_eleve(reponse_in: ReponseEleveCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle réponse d'élève.
    """
    reponse_service = ReponseEleveService(db)
    return reponse_service.enregistrer_reponse_eleve(reponse_in)

@router.get("/{id_reponse}", response_model=ReponseEleve)
async def lire_reponse_eleve(id_reponse: int, db: Session = Depends(get_db)):
    """
    Récupère une réponse d'élève par son ID.
    """
    reponse_service = ReponseEleveService(db)
    reponse = reponse_service.lire(id_reponse)
    if reponse is None:
        raise HTTPException(status_code=404, detail="Réponse de l'élève non trouvée")
    return reponse

@router.get("/", response_model=List[ReponseEleve])
async def lire_toutes_les_reponses_eleves(db: Session = Depends(get_db)):
    """
    Récupère toutes les réponses des élèves.
    """
    reponse_service = ReponseEleveService(db)
    reponses = reponse_service.lire_tous()
    return reponses

@router.put("/{id_reponse}", response_model=ReponseEleve)
async def mettre_a_jour_reponse_eleve(id_reponse: int, reponse_in: ReponseEleveCreate, db: Session = Depends(get_db)):
    """
    Met à jour une réponse d'élève existante.
    """
    reponse_service = ReponseEleveService(db)
    reponse = reponse_service.mettre_a_jour(id_reponse, reponse_in)
    if reponse is None:
        raise HTTPException(status_code=404, detail="Réponse de l'élève non trouvée")
    return reponse

@router.delete("/{id_reponse}", status_code=204)
async def supprimer_reponse_eleve(id_reponse: int, db: Session = Depends(get_db)):
    """
    Supprime une réponse d'élève par son ID.
    """
    reponse_service = ReponseEleveService(db)
    reponse = reponse_service.supprimer(id_reponse)
    if not reponse:
        raise HTTPException(status_code=404, detail="Réponse de l'élève non trouvée")
    return None