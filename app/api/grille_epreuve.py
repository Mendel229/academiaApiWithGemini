from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.image_utils import extract_text_from_image
from app.ai.grille_generator import generer_grille

router = APIRouter()

def create_response(success: bool, status: int, message):
    return JSONResponse(
        status_code=status,
        content={
            "success": success,
            "status": status,
            "message": message
        }
    )

@router.post("/completer_grille/", tags=["Generer grille"])
async def completer_grille(
    epreuve_file: UploadFile = File(...),
    prompt_grille: str = Form(None)
):
    if not epreuve_file:
        return create_response(False, 400, "Veuillez fournir l'épreuve.")

    try:
        epreuve_text = ""
        if epreuve_file.content_type.startswith("image/"):
            epreuve_text = await extract_text_from_image(epreuve_file.file)
        elif epreuve_file.content_type == "application/pdf":
            epreuve_text = extract_text_from_pdf(epreuve_file.file)
        else:
            return create_response(False, 400, "Format de l'épreuve non supporté (image ou PDF uniquement).")

        grille_completee = await generer_grille(epreuve_text, prompt_grille=prompt_grille)

        # Encodage JSON des données complexes
        data = {
            "grille_completee": grille_completee,
            "contenu_epreuve": epreuve_text,
            "prompt_utilisateur": prompt_grille
        }
        data_json = jsonable_encoder(data)

        return create_response(True, 200, data_json)
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de la génération de la grille : {str(e)}")
