from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, Dict, List

from app.models.copie_numerique import CopieNumeriqueDB, CopieNumeriqueCreate, CopieNumerique
from app.models.etudiant import EtudiantDB
from app.models.epreuve import EpreuveDB
from app.models.reponse_eleve import ReponseEleveDB, ReponseEleveCreate
from app.models.question import QuestionDB

class CopieNumeriqueService:
    """
    Service pour la gestion des copies numériques.
    Encapsule la logique métier liée aux copies numériques.
    """
    def __init__(self, db: Session):
        self.db = db

    def lire_tous(self):
        copies = self.db.query(CopieNumeriqueDB).all()
        return [copies]
    def enregistrer_copie_numerique(self, copie_in: CopieNumeriqueCreate) -> CopieNumerique:
        # Vérifier si l'étudiant existe
        etudiant = self.db.query(EtudiantDB).filter(EtudiantDB.id == copie_in.id_etudiant).first()
        if not etudiant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Étudiant avec l'ID '{copie_in.id_etudiant}' non trouvé")

        # Vérifier si l'épreuve existe
        epreuve = self.db.query(EpreuveDB).filter(EpreuveDB.id_epreuve == copie_in.id_epreuve).first()
        if not epreuve:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Épreuve avec l'ID '{copie_in.id_epreuve}' non trouvée")

        # Vérifier si une copie existe déjà
        existing_copie = self.db.query(CopieNumeriqueDB).filter(
            CopieNumeriqueDB.id_etudiant == copie_in.id_etudiant,
            CopieNumeriqueDB.id_epreuve == copie_in.id_epreuve
        ).first()
        if existing_copie:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Une copie existe déjà pour cet étudiant et cette épreuve")

        # Créer la copie numérique
        copie_db = CopieNumeriqueDB(**copie_in.model_dump())
        self.db.add(copie_db)
        self.db.commit()
        self.db.refresh(copie_db)
        return CopieNumerique.from_orm(copie_db)

    def enregistrer_copie_entiere(
        self,
        id_etudiant: int,
        id_epreuve: int,
        reponses_qcm: Dict[int, str],
        reponses_code: List[str],
        reponses_courtes: List[str]
    ) -> CopieNumerique:
        # Créer la copie numérique
        copie_create = CopieNumeriqueCreate(id_etudiant=id_etudiant, id_epreuve=id_epreuve)
        copie = self.enregistrer_copie_numerique(copie_create)

        # Récupérer toutes les questions de l'épreuve
        questions = self.db.query(QuestionDB).filter(QuestionDB.id_epreuve == id_epreuve).all()
        question_map = {q.id_question: q for q in questions}

        # Réponses QCM
        for id_question_str, reponse in reponses_qcm.items():
            id_question = int(id_question_str)
            if id_question in question_map:
                reponse_obj = ReponseEleveDB(
                    id_copie_numerique=copie.id_copie_numerique,
                    id_question=id_question,
                    reponse_choisie=reponse
                )
                self.db.add(reponse_obj)

        # Réponses Code
        code_questions = [q for q in questions if q.type_question == "code"]
        for i, question in enumerate(code_questions):
            if i < len(reponses_code):
                reponse_obj = ReponseEleveDB(
                    id_copie_numerique=copie.id_copie_numerique,
                    id_question=question.id_question,
                    reponse_libre=reponses_code[i]
                )
                self.db.add(reponse_obj)

        # Réponses Courtes
        courte_questions = [q for q in questions if q.type_question == "ouverte"]
        for i, question in enumerate(courte_questions):
            if i < len(reponses_courtes):
                reponse_obj = ReponseEleveDB(
                    id_copie_numerique=copie.id_copie_numerique,
                    id_question=question.id_question,
                    reponse_libre=reponses_courtes[i]
                )
                self.db.add(reponse_obj)

        self.db.commit()
        return copie
