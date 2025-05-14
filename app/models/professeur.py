from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.models.base import Base
from typing import Optional

class ProfesseurDB(Base):
    __tablename__ = "professeur"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    prenom: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    filiere: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    matiere: Mapped[str] = mapped_column(String)
    roles: Mapped[Optional[str]] = mapped_column(String, nullable=True)
