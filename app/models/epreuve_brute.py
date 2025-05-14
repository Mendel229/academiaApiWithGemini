from pydantic import BaseModel
from typing import Optional

class EpreuveTexte(BaseModel):
    texte_epreuve: str
    id_professeur: Optional[int]