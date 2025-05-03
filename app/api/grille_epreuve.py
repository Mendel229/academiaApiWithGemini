from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.image_utils import extract_text_from_image
from app.ai.grille_generator import generer_grille

router = APIRouter()

@router.post("/completer_grille/", tags=["Generer grille"])
async def completer_grille(
    epreuve_file: UploadFile = File(...),
    prompt_grille: str = Form(None)
):
    """
    Complète une grille de correction à partir d'une épreuve fournie (image ou PDF),
    en utilisant éventuellement un prompt personnalisé.
    """
    if not epreuve_file:
        raise HTTPException(status_code=400, detail="Veuillez fournir l'épreuve.")

    epreuve_text = ""
    if epreuve_file.content_type.startswith("image/"):
        epreuve_text = await extract_text_from_image(epreuve_file.file)
    elif epreuve_file.content_type == "application/pdf":
        epreuve_text = extract_text_from_pdf(epreuve_file.file)
    else:
        raise HTTPException(status_code=400, detail="Format de l'épreuve non supporté (image ou PDF uniquement).")

    grille_completee = await generer_grille(epreuve_text, prompt_grille=prompt_grille)
    
    return {
        "grille_completee": grille_completee,
        "contenu_epreuve": epreuve_text,
        "prompt_utilisateur": prompt_grille
    }
