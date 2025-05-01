from pydantic import BaseModel
from typing import List, Optional

class GenerationConstraints(BaseModel):
    matiere: str
    niveau: str
    duree: str
    Nombre_d_exercice: int
    objectifs: Optional[List[str]] = []
    prompt: Optional[str] = ""