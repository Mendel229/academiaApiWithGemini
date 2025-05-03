from app.ai.gemini_loader import load_gemini_model
import json

async def generer_grille(epreuve_text: str, prompt_grille: str = None) -> str:
    """
    Génère une grille de correction à partir du texte de l'épreuve,
    en utilisant éventuellement un prompt personnalisé.
    """
    model = load_gemini_model()
    prompt_base = f"""
    Analyse le texte de l'épreuve suivant et génère une grille de correction détaillée au format JSON.
    La grille doit contenir une liste d'exercices. Pour chaque exercice :
    - "numero": Le numéro de l'exercice (si identifiable).
    - "total_points": Le nombre total de points pour cet exercice (si identifiable).
    - "instructions": Les instructions spécifiques pour cet exercice (si présentes).
    - "questions": Une liste de questions dans cet exercice. Pour chaque question :
        - "question": Le texte exact de la question.
        - "type": Le type de question ("ouverte", "choix multiple", etc.).
        - "reponse_attendue": La réponse attendue (la plus précise possible). Pour les QCM, inclure les options et indiquer la bonne réponse.
        - "bareme": Le nombre de points attribués à cette question.

    Tente d'identifier la structure de l'épreuve (exercices, numéros de questions, barèmes partiels).
    Sois précis et concis dans les réponses attendues.

    Texte de l'épreuve :
    {epreuve_text}

    Grille de correction (JSON) :
    """

    if prompt_grille:
        prompt_final = f"{prompt_base}\n\nInstructions supplémentaires du professeur : {prompt_grille}"
    else:
        prompt_final = prompt_base

    try:
        response = model.generate_content(prompt_final)
        grille_json_str = response.text
        # Tentative de parsing pour s'assurer que c'est un JSON valide (peut échouer si l'IA ne respecte pas parfaitement le format)
        grille_data = json.loads(grille_json_str)
        return grille_json_str
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON de la réponse de l'IA : {e}")
        print(f"Réponse brute de l'IA : {grille_json_str}")
        # En cas d'erreur de parsing, retourne la chaîne brute pour inspection
        return grille_json_str
    except Exception as e:
        raise Exception(f"Erreur lors de la génération de la grille: {str(e)}")