from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from app.models.copie_numerique import CopieNumeriqueDB, CopieNumeriqueCreate, CopieNumerique  # Import des modèles
from app.models.etudiant import EtudiantDB  # Import du modèle Etudiant
from app.models.epreuve import EpreuveDB    # Import du modèle Epreuve


class CopieNumeriqueService:
    """
    Service pour la gestion des copies numériques.
    Encapsule la logique métier liée aux copies numériques.
    """
    def __init__(self, db: Session):
        """
        Initialise le service avec une session de base de données SQLAlchemy.

        Args:
            db: La session de la base de données SQLAlchemy.
        """
        self.db = db

    def enregistrer_copie_numerique(self, copie_in: CopieNumeriqueCreate) -> CopieNumerique:
        """
        Enregistre une nouvelle copie numérique dans la base de données.

        Args:
            copie_in: Les données de la copie à créer (depuis le schéma Pydantic).

        Returns:
            La copie numérique créée (sous forme de modèle SQLAlchemy).

        Raises:
            HTTPException: Si l'étudiant ou l'épreuve n'existe pas, ou si une copie existe déjà
                           pour cet étudiant et cette épreuve.
        """
        # Vérifier si l'étudiant existe
        etudiant = self.db.query(EtudiantDB).filter(EtudiantDB.id == copie_in.id_etudiant).first()
        if not etudiant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Étudiant avec l'ID '{copie_in.id_etudiant}' non trouvé")

        # Vérifier si l'épreuve existe
        epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == copie_in.id_epreuve).first()
        if not epreuve:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Épreuve avec l'ID '{copie_in.id_epreuve}' non trouvée")

        # Vérifier si une copie existe déjà pour cet étudiant et cette épreuve
        existing_copie = self.db.query(CopieNumeriqueDB).filter(CopieNumeriqueDB.id_etudiant == copie_in.id_etudiant, CopieNumeriqueDB.id_epreuve == copie_in.id_epreuve).first()
        if existing_copie:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Une copie existe déjà pour cet étudiant et cette épreuve")

        # Créer la copie numérique
        copie_db = CopieNumeriqueDB(**copie_in.model_dump())
        self.db.add(copie_db)
        self.db.commit()
        self.db.refresh(copie_db)
        return CopieNumerique.from_orm(copie_db) # Utilisation de from_orm
