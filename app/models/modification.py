from pydantic import BaseModel
from typing import Optional

class ModificationRequest(BaseModel):
    epreuve_initiale: str
    nouveau_prompt: str
    contenu_pdf: Optional[str] = None