from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session_examen import (
    SessionExamenCreate,
    SessionExamenRead,
    SessionExamenUpdate,
)
from app.services.session_examen_service import SessionExamenService
from app.utils.format_reponse import create_response

router = APIRouter(
    prefix="/api/exam-service/sessions",
    tags=["SessionExamen"]
)

@router.get("/", response_model=list[SessionExamenRead])
def list_sessions(db: Session = Depends(get_db)):
    service = SessionExamenService(db)
    items = service.list()
    payload = jsonable_encoder(items)
    return create_response(True, 200, payload)

@router.post("/", response_model=SessionExamenRead)
def create_session(session: SessionExamenCreate, db: Session = Depends(get_db)):
    service = SessionExamenService(db)
    obj = service.create(session)
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)

@router.get("/{id_session_examen}", response_model=SessionExamenRead)
def get_session(id_session_examen: int, db: Session = Depends(get_db)):
    service = SessionExamenService(db)
    obj = service.get(id_session_examen)
    if not obj:
        raise HTTPException(status_code=404, detail="Session d'examen non trouvée")
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)

@router.put("/{id_session_examen}", response_model=SessionExamenRead)
def update_session(
    id_session_examen: int,
    session: SessionExamenUpdate,
    db: Session = Depends(get_db),
):
    service = SessionExamenService(db)
    obj = service.update(id_session_examen, session)
    if not obj:
        raise HTTPException(status_code=404, detail="Session d'examen non trouvée")
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)

@router.delete("/{id_session_examen}")
def delete_session(id_session_examen: int, db: Session = Depends(get_db)):
    service = SessionExamenService(db)
    obj = service.delete(id_session_examen)
    if not obj:
        raise HTTPException(status_code=404, detail="Session d'examen non trouvée")
    payload = jsonable_encoder(obj)
    return create_response(True, 200, payload)
