from app.utils.pdf_utils import extract_text_from_pdf
from app.ai.gemini_loader import load_gemini_model
from app.ai.prompt_builder import build_prompt_from_constraints

def generate_exam(constraints: dict, pdf_file):
    """
    Génère une épreuve d'examen à partir de contraintes et d'un objet fichier PDF.
    """
    try:
        course_content = extract_text_from_pdf(pdf_file)
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction du texte depuis le PDF: {e}")

    prompt = build_prompt_from_constraints(course_content, constraints)

    model = load_gemini_model()
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du contenu avec Gemini: {e}")