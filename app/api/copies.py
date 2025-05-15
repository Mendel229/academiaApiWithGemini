from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.copie_numerique import CopieNumeriqueCreate, CopieNumeriqueUpdate
from app.services.copie_numerique_service import CopieNumeriqueService
from app.database import get_db
from app.utils.format_reponse import create_response

router = APIRouter(prefix="/copies", tags=["Copies Numériques"])


@router.post("/")
async def creer_copie(copie_in: CopieNumeriqueCreate, db: Session = Depends(get_db)):
    copie_service = CopieNumeriqueService(db)
    copie = copie_service.enregistrer_copie_numerique(copie_in)
    return create_response(True, 201, "Copie numérique créée avec succès")


@router.get("/{id_copie}")
async def lire_copie(id_copie: int, db: Session = Depends(get_db)):
    copie_service = CopieNumeriqueService(db)
    copie = copie_service.lire(id_copie)
    if copie is None:
        raise HTTPException(status_code=404, detail="Copie numérique non trouvée")
    data = jsonable_encoder(copie)
    return create_response(True, 200, data)


@router.get("/")
async def lire_toutes_les_copies(db: Session = Depends(get_db)):
    copie_service = CopieNumeriqueService(db)
    copies = copie_service.lire_tous()
    data = jsonable_encoder(copies)
    return create_response(True, 200, data)


@router.put("/{id_copie}")
async def mettre_a_jour_copie(id_copie: int, copie_in: CopieNumeriqueUpdate, db: Session = Depends(get_db)):
    copie_service = CopieNumeriqueService(db)
    copie = copie_service.mettre_a_jour(id_copie, copie_in)
    if copie is None:
        raise HTTPException(status_code=404, detail="Copie numérique non trouvée")
    return create_response(True, 200, "Copie mise à jour avec succès")


@router.delete("/{id_copie}")
async def supprimer_copie(id_copie: int, db: Session = Depends(get_db)):
    copie_service = CopieNumeriqueService(db)
    copie = copie_service.supprimer(id_copie)
    if not copie:
        raise HTTPException(status_code=404, detail="Copie numérique non trouvée")
    return create_response(True, 204, "Copie supprimée avec succès")
