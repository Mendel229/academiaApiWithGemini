import re
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

# Importer tes modèles SQLAlchemy ici
from app.models.epreuve import EpreuveDB
# from app.models.exercice import ExerciceDB # Décommenter si utilisé
from app.models.question import QuestionDB # Assure-toi que ce modèle est défini
from app.models.bonne_reponse import BonneReponseDB # Assure-toi que ce modèle est défini
# Assure-toi que ProfesseurDB est importé si nécessaire pour les relations,
# mais ici on utilise juste id_professeur
# from app.models.professeur import ProfesseurDB


class EnregistrementService:
    def __init__(self, db: Session):
        self.db = db

    def _parse_ai_output(self, texte_genere: str) -> Dict[str, Any]:
        parsed_data = {
            "epreuve_info": {},
            "exercices": [],
            "grille": []
        }
        current_section = None
        current_exercice_data = None
        current_question_data = None
        lines = texte_genere.splitlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line == "epreuve_debut":
                current_section = "epreuve"
                parsed_data["epreuve_info"] = {}
                continue
            elif line == "epreuve_fin":
                current_section = None
                continue
            elif line == "exo_debut":
                current_section = "exercice"
                current_exercice_data = {"questions": []}
                parsed_data["exercices"].append(current_exercice_data)
                continue
            elif line == "exo_fin":
                current_section = "epreuve"
                current_exercice_data = None
                continue
            elif line == "q_debut":
                current_section = "question"
                current_question_data = {"option": []}
                if current_exercice_data:
                    current_exercice_data["questions"].append(current_question_data)
                else:
                    print("⚠️ Question trouvée hors d'un bloc exercice. Elle sera ignorée si non gérée spécifiquement.")
                continue
            elif line == "q_fin":
                current_section = "exercice"
                current_question_data = None
                continue
            elif line == "grille_debut":
                current_section = "grille"
                parsed_data["grille"] = []
                continue
            elif line == "grille_fin":
                current_section = None
                break

            if ":" in line:
                key_raw, value = [s.strip() for s in line.split(":", 1)]
                key = key_raw.lower()

                if current_section == "epreuve" and current_question_data is None and current_exercice_data is None:
                    parsed_data["epreuve_info"][key] = value
                elif current_section == "exercice" and current_question_data is None:
                    if current_exercice_data is not None:
                        current_exercice_data[key] = value
                elif current_section == "question" and current_question_data is not None:
                    if key == "opt":
                        current_question_data["option"].append(value)
                    else:
                        current_question_data[key] = value
                elif current_section == "grille":
                    if key_raw == "ex": # Nouveau standard pour détecter une ligne de grille
                        grille_line_data = {}
                        parts = line.split("|")
                        for part_grille in parts: # Renommé 'part' en 'part_grille' pour éviter conflit
                            k_grille, v_grille = [s.strip() for s in part_grille.split(":", 1)]
                            grille_line_data[k_grille.lower()] = v_grille
                        parsed_data["grille"].append(grille_line_data)
        return parsed_data

    def enregistrer_epreuve_complete(self, texte_genere: str, id_professeur: Optional[int]) -> EpreuveDB | None:
        try:
            parsed_data = self._parse_ai_output(texte_genere)
            epreuve_info = parsed_data["epreuve_info"]

            titre_complet = epreuve_info.get("titre", "Épreuve sans titre")
            # La matière est implicite dans le titre ou non stockée séparément
            # _extracted_matiere = "N/A" # Variable locale si tu veux la logger
            parsed_niveau = "N/A"  # Valeur par défaut pour le niveau

            # Logique d'extraction du niveau à partir du titre
            # Format attendu: "Titre (contenant potentiellement la matière) - Niveau"
            # ou "Épreuve de {Matière} - {Niveau}"
            titre_match_detail = re.search(r'Épreuve de\s+(.+?)\s+-\s*(.+)', titre_complet, re.IGNORECASE)
            if titre_match_detail:
                # _extracted_matiere = titre_match_detail.group(1).strip()
                parsed_niveau = titre_match_detail.group(2).strip()
            elif " - " in titre_complet:
                parts = titre_complet.split(" - ", 1)
                if len(parts) == 2:
                    # Si "Épreuve de..." est dans la première partie, la seconde est le niveau
                    if parts[0].lower().startswith("épreuve de"):
                        # _extracted_matiere = parts[0][len("épreuve de"):].strip()
                        parsed_niveau = parts[1].strip()
                    else: # Sinon, on suppose "Titre quelconque/Matière - Niveau"
                        # _extracted_matiere = parts[0].strip()
                        parsed_niveau = parts[1].strip()

            # Si l'IA fournit un champ "niveau:" directement dans epreuve_info, il pourrait avoir priorité
            # Cependant, ton prompt actuel ne le demande pas explicitement pour epreuve_debut.
            # Donc, on se fie principalement au parsing du titre pour le niveau.
            final_niveau = epreuve_info.get("niveau", parsed_niveau).strip() # Priorise info explicite si elle existe

            db_epreuve = EpreuveDB(
                titre=titre_complet.strip(),
                duree=epreuve_info.get("duree", "N/A").strip(),
                niveau=final_niveau,
                id_professeur=id_professeur
                # created_at est géré par default=func.now()
            )
            self.db.add(db_epreuve)
            self.db.flush()

            print(f"ℹ️ Épreuve '{db_epreuve.titre}' (Niveau: {db_epreuve.niveau}) prête avec ID (futur) {db_epreuve.id_epreuve}")

            all_questions_db_objects = []
            for exo_data in parsed_data.get("exercices", []):
                # Optionnel: enregistrer l'exercice si modèle ExerciceDB
                # ...
                for q_data in exo_data.get("questions", []):
                    # Assure-toi que QuestionDB a les champs :
                    # type_question, contenu, option (JSON), id_epreuve
                    db_question = QuestionDB(
                        type_question=q_data.get("type", "ouverte").lower(),
                        contenu=q_data.get("contenu", "Contenu manquant"),
                        option=q_data.get("option") if q_data.get("type", "").lower() == "qcm" else None,
                        id_epreuve=db_epreuve.id_epreuve,
                    )
                    self.db.add(db_question)
                    all_questions_db_objects.append(db_question)

            self.db.flush()

            question_id_map_for_grille = {
                i + 1: q_db.id_question for i, q_db in enumerate(all_questions_db_objects)
            }

            for item_grille in parsed_data.get("grille", []):
                try:
                    q_num_in_grille = int(item_grille.get("q"))
                    id_question_cible = question_id_map_for_grille.get(q_num_in_grille)

                    if id_question_cible:
                        contenu_reponse = item_grille.get("rep") # Pour QCM
                        if not contenu_reponse:
                            contenu_reponse = item_grille.get("attendu") # Pour ouverte/code

                        if contenu_reponse is None:
                            print(f"⚠️ Réponse/attendu manquant pour q:{q_num_in_grille} de la grille.")
                            continue

                        # Assure-toi que BonneReponseDB a les champs :
                        # contenu_reponse, bareme, id_question
                        db_bonne_reponse = BonneReponseDB(
                            contenu_reponse=contenu_reponse,
                            bareme=float(item_grille.get("bareme", 0.0)),
                            id_question=id_question_cible
                        )
                        self.db.add(db_bonne_reponse)
                    else:
                        print(f"⚠️ Impossible de mapper q:{q_num_in_grille} de la grille à une question DB.")
                except ValueError:
                    print(f"⚠️ Ligne de grille malformée (q ou bareme non numérique): {item_grille}")
                except Exception as e_grille:
                    print(f"❌ Erreur item grille {item_grille}: {e_grille}")

            self.db.commit()
            self.db.refresh(db_epreuve)
            print(f"✅ Épreuve ID {db_epreuve.id_epreuve} enregistrée.")
            return db_epreuve

        except Exception as e:
            self.db.rollback()
            print(f"❌ Erreur majeure enregistrement épreuve: {e}")
            import traceback
            traceback.print_exc()
            return None