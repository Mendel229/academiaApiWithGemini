from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.save_epreuve_service import EnregistrementService
from app.models.epreuve_brute import EpreuveTexte

router = APIRouter()

@router.post("/enregistrer_epreuve/")
async def enregistrer_epreuve_endpoint(
    epreuve_data: EpreuveTexte,
    db: Session = Depends(get_db),
):
    """
    Enregistre une épreuve à partir du texte généré, en associant un professeur.
    """
    enregistrement_service = EnregistrementService(db)
    id_professeur = epreuve_data.id_professeur 
    if id_professeur is None:
        raise HTTPException(status_code=400, detail="L'ID du professeur est requis pour enregistrer une épreuve.")
    epreuve_db = enregistrement_service.enregistrer_epreuve(epreuve_data.texte_epreuve, id_professeur)
    if epreuve_db:
        return {"message": "Épreuve enregistrée avec succès.", "id_epreuve": epreuve_db.id_epreuve}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement de l'épreuve.")
