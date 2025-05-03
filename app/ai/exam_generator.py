from app.ai.gemini_loader import load_gemini_model
from app.ai.prompt_builder import build_prompt_from_constraints


def generate_exam(constraints: dict, course_content: str):
    """
    Génère une épreuve d'examen à partir de contraintes et du contenu texte extrait du PDF.
    """
    prompt = build_prompt_from_constraints(course_content, constraints)

    model = load_gemini_model()
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du contenu avec Gemini: {e}")