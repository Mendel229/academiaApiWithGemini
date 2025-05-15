from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
import re

from app.models.copie_numerique import CopieNumeriqueDB
from app.ai.gemini_loader import load_gemini_model
from app.ai.correction_ai import construire_prompt_correction
from app.models.question import QuestionDB
from app.models.bonne_reponse import BonneReponseDB
from app.models.reponse_eleve import ReponseEleveDB


class CorrectionService:
    def __init__(self, db: Session):
        self.db = db
        self.model = load_gemini_model()

    def corriger_copie(self, id_copie_numerique: int) -> Optional[float]:
        """
        Corrige une copie numérique en utilisant un modèle de langage.
        """
        copie_numerique_db = self.db.query(CopieNumeriqueDB).filter(
            CopieNumeriqueDB.id_copie_numerique == id_copie_numerique
        ).first()
        if not copie_numerique_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Copie numérique avec l'ID '{id_copie_numerique}' non trouvée",
            )

        reponses_eleve = (
            self.db.query(ReponseEleveDB)
            .filter(ReponseEleveDB.id_copie_numerique == id_copie_numerique)
            .all()
        )
        if not reponses_eleve:
            print(f"⚠️ Aucune réponse trouvée pour la copie ID '{id_copie_numerique}'.")
            return 0.0

        questions = (
            self.db.query(QuestionDB).filter(QuestionDB.id_epreuve == copie_numerique_db.id_epreuve).all()
        )
        bonnes_reponses = (
            self.db.query(BonneReponseDB)
            .join(QuestionDB)
            .filter(QuestionDB.id_epreuve == copie_numerique_db.id_epreuve)
            .all()
        )

        if not questions or not bonnes_reponses:
            print(
                f"⚠️ Aucune question ou bonne réponse trouvée pour l'épreuve ID '{copie_numerique_db.id_epreuve}'."
            )
            return 0.0

        # Utiliser la fonction du module ai pour construire le prompt
        prompt = construire_prompt_correction(questions, bonnes_reponses, reponses_eleve)

        try:
            #  Appeler le modèle chargé pour obtenir la réponse
            response = self.model.generate_content(prompt)
            note_str = response.text
            # Extraction de la note (peut nécessiter une logique plus robuste)
            match = re.search(r"Note de l'étudiant:\s*([\d.]+)", note_str, re.IGNORECASE)
            if match:
                note = float(match.group(1))
                return note
            else:
                print(
                    f"❌ Impossible d'extraire la note de la réponse du modèle: '{note_str}'"
                )
                return None

        except Exception as e:
            print(f"❌ Erreur lors de la communication avec le modèle de langage: {e}")
            return None
