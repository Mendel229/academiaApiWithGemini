from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from app.models.base import Base
from typing import Optional, TYPE_CHECKING

class ProfesseurDB(Base):
    __tablename__ = "professeur"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    prenom: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    filiere: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    matiere: Mapped[str] = mapped_column(String, nullable=False)
    roles: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    enseignements = relationship("EnseignementDB", back_populates="professeur")

    
