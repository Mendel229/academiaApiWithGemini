from typing import List
from app.models.question import QuestionDB
from app.models.bonne_reponse import BonneReponseDB
from app.models.reponse_eleve import ReponseEleveDB


def construire_prompt_correction(
    questions: List[QuestionDB],
    bonnes_reponses: List[BonneReponseDB],
    reponses_eleve: List[ReponseEleveDB],
) -> str:
    """
    Construit le prompt pour le modèle de langage pour la correction.
    """
    prompt = "Voici l'épreuve, le barème et les réponses de l'étudiant. Base-toi sur le barème pour corriger la copie de l'étudiant et retourne uniquement la note finale.\n\n"
    prompt += "**Épreuve:**\n"
    for question in questions:
        prompt += f"- Question (ID: {question.id_question}, Type: {question.type_question}): {question.contenu}\n"
        if question.option:
            prompt += f"  Options: {question.option}\n"

    prompt += "\n**Barème:**\n"
    for bonne_reponse in bonnes_reponses:
        prompt += f"- Question ID: {bonne_reponse.id_question}, Bonne Réponse: '{bonne_reponse.bonne_reponse}', Barème: {bonne_reponse.bareme}\n"

    prompt += "\n**Réponses de l'étudiant:**\n"
    for reponse in reponses_eleve:
        question_texte = next(
            (q.contenu for q in questions if q.id_question == reponse.id_question),
            "Question non trouvée",
        )
        prompt += (
            f"- Question ID: {reponse.id_question}, Réponse de l'étudiant: '{reponse.reponse}', Question: '{question_texte}'\n"
        )

    prompt += "\n**Consigne:** Corrige attentivement chaque réponse de l'étudiant en te basant sur le barème fourni. Retourne uniquement la note finale de l'étudiant sous le format 'Note de l'étudiant: [note]'. Ne donne aucune autre explication."
    return prompt
