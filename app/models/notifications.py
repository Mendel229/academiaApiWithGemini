# app/models/notifications.py
from sqlalchemy import String, Integer, Boolean, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from pydantic import BaseModel
from app.models.base import Base

# Pydantic Schemas
class NotificationBase(BaseModel):
    message: str
    est_lue: bool
    type_notification: str
    role_utilisateur: str
    date_reception: datetime

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# SQLAlchemy Model
class NotificationsDB(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    est_lue: Mapped[bool] = mapped_column(Boolean, nullable=False)
    type_notification: Mapped[str] = mapped_column(Text, nullable=False)
    role_utilisateur: Mapped[str] = mapped_column(Text, nullable=False)
    date_reception: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
