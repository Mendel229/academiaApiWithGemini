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
    Inclut un exemple et des consignes strictes pour réduire la variabilité des notes.
    """
    prompt = (
        "Tu es un correcteur automatique. Voici un exemple de correction pour te guider :\n\n"
        "**Exemple :**\n"
        "**Épreuve :**\n"
        "- Question (ID: 1, Type: qcm): Quelle est la capitale de la France ?\n"
        "  Options: [Paris, Lyon, Marseille, Lille]\n\n"
        "**Barème :**\n"
        "- Question ID: 1, Bonne Réponse: 'Paris', Barème: 2\n\n"
        "**Réponses de l'étudiant :**\n"
        "- Question ID: 1, Réponse de l'étudiant: 'Paris', Question: 'Quelle est la capitale de la France ?'\n\n"
        "**Résultat attendu :**\n"
        "Note de l'étudiant: [2.00]\n\n"
        "------------------------\n\n"
        "Corrige maintenant la copie suivante de la même manière.\n"
    )

    prompt += "\n**Épreuve :**\n"
    for question in questions:
        prompt += f"- Question (ID: {question.id_question}, Type: {question.type_question}): {question.contenu}\n"
        if question.option:
            prompt += f"  Options: {question.option}\n"

    prompt += "\n**Barème :**\n"
    for bonne_reponse in bonnes_reponses:
        prompt += f"- Question ID: {bonne_reponse.id_question}, Bonne Réponse: '{bonne_reponse.bonne_reponse}', Barème: {bonne_reponse.bareme}\n"

    prompt += "\n**Réponses de l'étudiant :**\n"
    for reponse in reponses_eleve:
        question_texte = next(
            (q.contenu for q in questions if q.id_question == reponse.id_question),
            "Question non trouvée",
        )

        contenu_reponse = reponse.reponse_choisie or reponse.reponse_libre or "Aucune réponse"
        prompt += (
            f"- Question ID: {reponse.id_question}, Réponse de l'étudiant: '{contenu_reponse}', Question: '{question_texte}'\n"
        )

    prompt += (
        "\n**Consigne stricte :**\n"
        "Corrige chaque réponse avec rigueur en te basant uniquement sur le barème fourni. "
        "Attribue exactement les points prévus. Ne donne aucune explication. "
        "Ne fais preuve d'aucune subjectivité. Si la réponse est incorrecte ou absente, mets 0 point. "
        "Ta correction doit être cohérente, stable et reproductible.\n\n"
        "Retourne uniquement la note finale, sous le format strict suivant (ne rien ajouter d'autre) :\n"
        "Note de l'étudiant: [x.xx]"
    )

    return prompt
