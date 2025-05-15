from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.correction_service import CorrectionService
from app.models.copie_numerique import CopieNumeriqueDB, CopieNumerique

router = APIRouter(prefix="/corrections", tags=["Corrections copie numérique"])


@router.post("/copies/{id_copie}/corriger", response_model=CopieNumerique)
async def corriger_copie_endpoint(
    id_copie: int, db: Session = Depends(get_db)
) -> CopieNumerique:
    """
    Déclenche la correction d'une copie numérique spécifique.
    """
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
        # Mise à jour de la copie numérique avec la note finale et le statut
        copie_numerique_db.note_finale = note_finale
        copie_numerique_db.statut = True  # Marquer la copie comme corrigée
        db.commit()
        db.refresh(copie_numerique_db)
        return CopieNumerique.from_orm(copie_numerique_db)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Copie numérique avec l'ID '{id_copie}' non trouvée.",
        )
