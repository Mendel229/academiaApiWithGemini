from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.correction_service import CorrectionService
from app.models.copie_numerique import CopieNumeriqueDB
from app.utils.format_reponse import create_response

router = APIRouter(prefix="/corrections", tags=["Corrections copie numérique"])


@router.post("/copies/{id_copie}/corriger")
async def corriger_copie_endpoint(id_copie: int, db: Session = Depends(get_db)):
    correction_service = CorrectionService(db)
    note_finale = correction_service.corriger_copie(id_copie)
    if note_finale is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la correction de la copie.",
        )

    copie_numerique_db = (
        db.query(CopieNumeriqueDB)
        .filter(CopieNumeriqueDB.id_copie_numerique == id_copie)
        .first()
    )
    if copie_numerique_db:
        copie_numerique_db.note_finale = note_finale
        copie_numerique_db.statut = True
        db.commit()
        db.refresh(copie_numerique_db)
        data = jsonable_encoder(copie_numerique_db)
        return create_response(True, 200, data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Copie numérique avec l'ID '{id_copie}' non trouvée.",
        )
