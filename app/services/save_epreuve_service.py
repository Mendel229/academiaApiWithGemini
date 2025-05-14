import re
from sqlalchemy.orm import Session
from app.models.epreuve import EpreuveDB
from app.models.question import QuestionDB
from app.models.bonne_reponse import BonneReponseDB
from typing import List

class EnregistrementService:
    def __init__(self, db: Session):
        self.db = db

    def enregistrer_epreuve(self, texte_genere: str, id_professeur: int) -> EpreuveDB | None:
        try:
            titre_match = re.search(r'titre:\s*Épreuve de (.+?)\s*-\s*(.+)', texte_genere)
            duree_match = re.search(r'duree:\s*(.+)', texte_genere)
            if not titre_match or not duree_match:
                raise ValueError("Impossible d'extraire les informations de l'épreuve.")
            matiere = titre_match.group(1).strip()
            niveau = titre_match.group(2).strip()
            duree = duree_match.group(1).strip()

            db_epreuve = EpreuveDB(titre=f"Épreuve de {matiere} - {niveau}", duree=duree, niveau=niveau, id_professeur=id_professeur) # Ajout id_professeur
            self.db.add(db_epreuve)
            self.db.commit()
            self.db.refresh(db_epreuve)
            print(f"✅ Épreuve enregistrée avec ID {db_epreuve.id_epreuve}")
            self.enregistrer_questions_et_reponses(texte_genere, db_epreuve.id_epreuve)
            return db_epreuve
        except Exception as e:
            self.db.rollback()
            print(f"❌ Erreur lors de l'enregistrement de l'épreuve : {e}")
            return None

    def enregistrer_questions_et_reponses(self, texte_genere: str, id_epreuve: int):
        try:
            questions_data = self._extraire_questions(texte_genere)
            id_question_map = {}

            for idx, question_data in enumerate(questions_data):
                db_question = QuestionDB(
                    type_question=question_data["type"],
                    contenu=question_data["contenu"],
                    option=question_data["options"] if question_data["options"] else None,
                    id_epreuve=id_epreuve
                )
                self.db.add(db_question)
                self.db.commit()
                self.db.refresh(db_question)
                id_question_map[idx + 1] = db_question.id_question

            self._enregistrer_bonnes_reponses(texte_genere, id_question_map)
            print("✅ Questions et réponses enregistrées avec succès.")
        except Exception as e:
            self.db.rollback()
            print(f"❌ Erreur lors de l'enregistrement des questions/réponses : {e}")

    def _extraire_questions(self, texte_genere: str) -> List[dict]:
        questions = []
        current_question = {}
        in_question = False
        lines = texte_genere.splitlines()
        for line in lines:
            line = line.strip()
            if line == "q_debut":
                current_question = {"options": []}
                in_question = True
            elif line == "q_fin":
                questions.append(current_question)
                in_question = False
            elif in_question:
                if line.startswith("type:"):
                    current_question["type"] = line.replace("type:", "").strip()
                elif line.startswith("contenu:"):
                    current_question["contenu"] = line.replace("contenu:", "").strip()
                elif line.startswith("opt:"):
                    option = line.replace("opt:", "").strip()
                    current_question["options"].append(option)
        return questions

    def _enregistrer_bonnes_reponses(self, texte_genere: str, id_question_map: dict):
        in_grille = False
        lines = texte_genere.splitlines()
        for line in lines:
            line = line.strip()
            if line == "grille_debut":
                in_grille = True
                continue
            elif line == "grille_fin":
                break

            if in_grille and line.startswith("ex:"):
                parts = line.split("|")
                ex = int(parts[0].split(":")[1].strip())
                q = int(parts[1].split(":")[1].strip())
                type_q = parts[2].split(":")[1].strip()
                bareme = float(parts[-1].split(":")[1].strip())

                id_question = id_question_map.get(q)
                if not id_question:
                    continue

                bonne_rep_str = parts[3].split(":")[1].strip()
                db_bonne_reponse = BonneReponseDB(
                    bonne_reponse=bonne_rep_str,
                    bareme=bareme,
                    id_question=id_question
                )
                self.db.add(db_bonne_reponse)
        self.db.commit()