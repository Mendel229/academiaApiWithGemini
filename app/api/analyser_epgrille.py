from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf_utils import extract_text_from_pdf
from app.ai.balisage_epreuve import baliser_epreuve

router = APIRouter()

@router.post("/analyser_epreuve_avec_grille/")
async def analyser_epreuve_avec_grille(
    pdf_file: UploadFile = File(...)
):
    """
    Analyse un PDF contenant l'épreuve et la grille de correction balisée par l'IA.
    """
    if not pdf_file:
        raise HTTPException(status_code=400, detail="Veuillez fournir le fichier PDF contenant l'épreuve et la grille.")

    try:
        pdf_text = extract_text_from_pdf(pdf_file.file)
        resultats_balisage = await baliser_epreuve(pdf_text)
        return {"epreuve_balisee": resultats_balisage["epreuve_balisee"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse et du balisage de l'épreuve: {str(e)}")