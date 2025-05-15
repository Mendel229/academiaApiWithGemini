from fastapi import APIRouter, UploadFile, File
from fastapi.encoders import jsonable_encoder
from app.utils.pdf_utils import extract_text_from_pdf
from app.ai.balisage_epreuve import baliser_epreuve
from app.utils.format_reponse import create_response

router = APIRouter()

@router.post("/analyser_epreuve_avec_grille/")
async def analyser_epreuve_avec_grille(
    pdf_file: UploadFile = File(...)
):
    """
    Analyse un PDF contenant l'épreuve et la grille de correction balisée par l'IA.
    """
    if not pdf_file:
        return create_response(False, 400, "Veuillez fournir le fichier PDF contenant l'épreuve et la grille.")

    try:
        pdf_text = extract_text_from_pdf(pdf_file.file)
        resultats_balisage = await baliser_epreuve(pdf_text)
        data = jsonable_encoder({"epreuve_balisee": resultats_balisage["epreuve_balisee"]})
        return create_response(True, 200, data)
    except Exception as e:
        return create_response(False, 500, f"Erreur lors de l'analyse et du balisage de l'épreuve: {str(e)}")
