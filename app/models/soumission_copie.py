from pydantic import BaseModel
from typing import Dict, List

class SoumissionCopieNumerique(BaseModel):
    id_etudiant: int
    id_epreuve: int
    reponses_qcm: Dict[int, str]       # id_question: réponse choisie
    reponses_code: List[str]           # Réponses dans l’ordre des questions code
    reponses_courtes: List[str]        # Réponses dans l’ordre des questions ouvertes
