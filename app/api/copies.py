from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.models.copie_numerique import CopieNumeriqueDB, CopieNumeriqueCreate, CopieNumerique, CopieNumeriqueUpdate # Importez le schéma Pydantic CopieNumerique
from app.services.copie_numerique_service import CopieNumeriqueService
from app.database import get_db

router = APIRouter(prefix="/copies", tags=["Copies Numériques"])

@router.post("/", response_model=CopieNumerique, status_code=201)
async def creer_copie(copie_in: CopieNumeriqueCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle copie numérique.
    """
    copie_service = CopieNumeriqueService(db)
    return copie_service.enregistrer_copie_numerique(copie_in)

@router.get("/{id_copie}", response_model=CopieNumerique) # Utilisez le schéma Pydantic CopieNumerique
async def lire_copie(id_copie: int, db: Session = Depends(get_db)):
    """
    Récupère une copie numérique par son ID.
    """
    copie_service = CopieNumeriqueService(db)
    copie = copie_service.lire(id_copie)
    if copie is None:
        raise HTTPException(status_code=404, detail="Copie numérique non trouvée")
    return copie

@router.get("/", response_model=List[CopieNumerique]) # Utilisez le schéma Pydantic CopieNumerique
async def lire_toutes_les_copies(db: Session = Depends(get_db)):
    """
    Récupère toutes les copies numériques.
    """
    copie_service = CopieNumeriqueService(db)
    copies = copie_service.lire_tous()
    return copies

@router.put("/{id_copie}", response_model=CopieNumerique) # Utilisez le schéma Pydantic CopieNumerique
async def mettre_a_jour_copie(id_copie: int, copie_in: CopieNumeriqueUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une copie numérique existante.
    """
    copie_service = CopieNumeriqueService(db)
    copie = copie_service.mettre_a_jour(id_copie, copie_in)
    if copie is None:
        raise HTTPException(status_code=404, detail="Copie numérique non trouvée")
    return copie

@router.delete("/{id_copie}", status_code=204)
async def supprimer_copie(id_copie: int, db: Session = Depends(get_db)):
    """
    Supprime une copie numérique par son ID.
    """
    copie_service = CopieNumeriqueService(db)
    copie = copie_service.supprimer(id_copie)
    if not copie:
        raise HTTPException(status_code=404, detail="Copie numérique non trouvée")
    return None
