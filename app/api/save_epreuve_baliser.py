from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.save_epreuve_manuelly_service import EnregistrementService
from app.models.epreuve_brute import EpreuveTexte
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.format_reponse import create_response

router = APIRouter(tags=["Enregistrer une épreuve manuelle baliser"])

@router.post("/enregistrer_epreuve/manually")
async def enregistrer_epreuve_endpoint(
    epreuve_data: EpreuveTexte,
    db: Session = Depends(get_db),
):
    enregistrement_service = EnregistrementService(db)
    id_professeur = epreuve_data.id_professeur 
    if id_professeur is None:
        return create_response(False, 400, "L'ID du professeur est requis pour enregistrer une épreuve.")
    
    epreuve_db = enregistrement_service.enregistrer_epreuve_complete(epreuve_data.texte_epreuve, id_professeur)
    if epreuve_db:
        contenu = {
            "message": "Épreuve enregistrée avec succès.",
            "id_epreuve": epreuve_db.id_epreuve
        }
        contenu_json = jsonable_encoder(contenu)  # <-- encodage JSON (utile surtout si epreuve_db.id_epreuve n'est pas un type natif)
        return create_response(True, 201, contenu_json)
    else:
        return create_response(False, 500, "Erreur lors de l'enregistrement de l'épreuve.")
