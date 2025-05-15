from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.models.base import Base
from app.models.copie_numerique import CopieNumeriqueDB

class EtudiantDB(Base):
    """
    Modèle SQLAlchemy pour la table 'etudiant'.
    """
    __tablename__ = "etudiant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    matricule: Mapped[str] = mapped_column(String)

    copies_numeriques: Mapped[List["CopieNumeriqueDB"]] = relationship(
        "CopieNumeriqueDB", back_populates="etudiant", cascade="all, delete-orphan"
    )
    
