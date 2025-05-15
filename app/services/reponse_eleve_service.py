from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from app.models.reponse_eleve import ReponseEleveDB, ReponseEleveCreate, ReponseEleve  # Import des modèles
from app.models.copie_numerique import CopieNumeriqueDB
from app.models.question import QuestionDB


class ReponseEleveService:
    """
    Service pour la gestion des réponses des élèves.
    Encapsule la logique métier liée aux réponses des élèves.
    """
    def __init__(self, db: Session):
        """
        Initialise le service avec une session de base de données SQLAlchemy.

        Args:
            db: La session de la base de données SQLAlchemy.
        """
        self.db = db

    def enregistrer_reponse_eleve(self, reponse_in: ReponseEleveCreate) -> ReponseEleve:
        """
        Enregistre une nouvelle réponse d'élève dans la base de données.

        Args:
            reponse_in: Les données de la réponse de l'élève à créer (depuis le schéma Pydantic).

        Returns:
            La réponse de l'élève créée.

        Raises:
            HTTPException: Si la copie numérique ou la question n'existe pas.
        """
        # Vérifier si la copie numérique existe
        copie_numerique = self.db.query(CopieNumeriqueDB).filter(CopieNumeriqueDB.id_copie_numerique == reponse_in.id_copie_numerique).first()
        if not copie_numerique:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Copie numérique avec l'ID '{reponse_in.id_copie_numerique}' non trouvée")

        # Vérifier si la question existe
        question = self.db.query(QuestionDB).filter(QuestionDB.id_question == reponse_in.id_question).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question avec l'ID '{reponse_in.id_question}' non trouvée")

        # Créer la réponse de l'élève
        reponse_db = ReponseEleveDB(**reponse_in.model_dump())
        self.db.add(reponse_db)
        self.db.commit()
        self.db.refresh(reponse_db)
        return ReponseEleve.from_orm(reponse_db)
