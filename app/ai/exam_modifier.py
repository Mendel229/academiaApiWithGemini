# app/ai/exam_modifier.py
from app.ai.gemini_loader import load_gemini_model

def modify_exam(epreuve_initiale: str, nouveau_prompt: str, contenu_pdf: str) -> str:
    """
    Prend l'épreuve initiale, le nouveau prompt et le contenu du PDF,
    et renvoie l'épreuve modifiée par l'IA.
    """
    # CONSTRUIRE LE PROMPT POUR L'IA
    prompt_ia = f"""Voici l'épreuve initiale que tu m'avais générée :
    {epreuve_initiale}

    Voici le contenu du document source :
    {contenu_pdf}

    Le professeur souhaite apporter les modifications suivantes :
    {nouveau_prompt}

    Modifie l'épreuve en conséquence, en conservant le même système de balisage ('q_debut', 'type:', 'contenu:', 'opt:', 'q_fin', 'grille_debut', 'ex:', etc.).
    """

    # CHARGER LE MODÈLE GEMINI
    model = load_gemini_model()

    # ENVOYER LE PROMPT AU MODÈLE D'IA
    try:
        response = model.generate_content(prompt_ia)
        return response.text
    except Exception as e:
        raise Exception(f"Erreur lors de la génération du contenu avec Gemini pour la modification: {e}")