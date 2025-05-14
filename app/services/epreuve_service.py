from sqlalchemy.orm import Session
from typing import List
from app.models.epreuve import Epreuve, EpreuveCreate, EpreuveDB

class EpreuveService:
    def __init__(self, db: Session):
        self.db = db

    def creer(self, epreuve_in: EpreuveCreate) -> Epreuve:
        """Crée une nouvelle épreuve."""
        db_epreuve = EpreuveDB(
            titre=epreuve_in.titre,
            duree=epreuve_in.duree,
            niveau=epreuve_in.niveau,
            id_professeur=epreuve_in.id_professeur  # Ajout de l'id_professeur
        )
        self.db.add(db_epreuve)
        self.db.commit()
        self.db.refresh(db_epreuve)
        return Epreuve.from_orm(db_epreuve)

    def lire(self, id_epreuve: int) -> Epreuve | None:
        """Récupère une épreuve par son ID."""
        epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == id_epreuve).first()
        if epreuve:
            return Epreuve.from_orm(epreuve)
        return None

    def lire_tous(self) -> List[Epreuve]:
        """Récupère toutes les épreuves."""
        epreuves = self.db.query(EpreuveDB).all()
        return [Epreuve.from_orm(epreuve) for epreuve in epreuves]

    def mettre_a_jour(self, id_epreuve: int, epreuve_in: EpreuveCreate) -> Epreuve | None:
        """Met à jour une épreuve existante."""
        db_epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == id_epreuve).first()
        if db_epreuve:
            db_epreuve.titre = epreuve_in.titre
            db_epreuve.duree = epreuve_in.duree
            db_epreuve.niveau = epreuve_in.niveau
            db_epreuve.id_professeur = epreuve_in.id_professeur # Mise à jour id_professeur
            self.db.commit()
            self.db.refresh(db_epreuve)
            return Epreuve.from_orm(db_epreuve)
        return None

    def supprimer(self, id_epreuve: int):
        """Supprime une épreuve par son ID."""
        epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == id_epreuve).first()
        if epreuve:
            self.db.delete(epreuve)
            self.db.commit()