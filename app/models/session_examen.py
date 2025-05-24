# app/models/session_examen.py
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from app.models.base import Base

class SessionExamenDB(Base):
    __tablename__ = "session_examen"

    id_session_examen: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    nom_session: Mapped[str] = mapped_column(String(255), nullable=False)
    date_debut_session: Mapped[Date] = mapped_column(Date, nullable=False)
    date_fin_session: Mapped[Date] = mapped_column(Date, nullable=False)
    statut_session: Mapped[str] = mapped_column(String(50), nullable=False, server_default="Planifiée")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("exam_service.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

# Pydantic schemas
from pydantic import BaseModel, ConfigDict
from datetime import date

class SessionExamenBase(BaseModel):
    nom_session: str
    date_debut_session: date
    date_fin_session: date
    statut_session: str | None = None
    created_by: int | None = None

class SessionExamenCreate(SessionExamenBase):
    pass

class SessionExamenUpdate(SessionExamenBase):
    nom_session: str | None = None
    date_debut_session: date | None = None
    date_fin_session: date | None = None
    statut_session: str | None = None
    created_by: int | None = None

class SessionExamenRead(SessionExamenBase):
    id_session_examen: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)