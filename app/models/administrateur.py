from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from pydantic import BaseModel
from app.models.base import Base

# SQLAlchemy Model
class AdministrateurDB(Base):
    __tablename__ = "administrateur"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    roles: Mapped[Optional[str]] = mapped_column(String, nullable=True)

# Pydantic Schemas
class AdministrateurBase(BaseModel):
    login: str
    password: str
    roles: Optional[str] = None

class AdministrateurCreate(AdministrateurBase):
    pass

class AdministrateurRead(AdministrateurBase):
    id: int

    class Config:
        orm_mode = True
