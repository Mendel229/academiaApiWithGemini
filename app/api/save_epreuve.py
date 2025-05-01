from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from app.models.epreuve_brute import EpreuveTexte
from app.services.save_epreuve_service import EnregistrementService
from app.database import get_db

router = APIRouter(tags=["Enregistrement"])

@router.post("/enregistrer_epreuve/")
async def enregistrer_epreuve_endpoint(epreuve_data: EpreuveTexte, db: Session = Depends(get_db)):
    enregistrement_service = EnregistrementService(db)
    epreuve_db = enregistrement_service.enregistrer_epreuve(epreuve_data.texte_epreuve)
    if epreuve_db:
        return {"message": f"Épreuve enregistrée avec succès, ID: {epreuve_db.id_epreuve}"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de l'enregistrement de l'épreuve.")