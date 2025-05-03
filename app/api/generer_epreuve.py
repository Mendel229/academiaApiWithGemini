from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Body
from typing import Dict
import json
from app.ai.exam_generator import generate_exam
from app.models.generation import GenerationConstraints
from app.ai.exam_modifier import modify_exam
from app.models.modification import ModificationRequest
from app.utils.pdf_utils import extract_text_from_pdf
import traceback

router = APIRouter()

@router.post("/generer_epreuve/")
async def generer_epreuve(
    pdf_file: UploadFile = File(...),
    constraints: str = Form(...)
):
    """
    Génère une épreuve d'examen à partir d'un fichier PDF et de contraintes JSON envoyées en tant que chaîne.
    Renvoie l'épreuve et le texte extrait du PDF.
    """
    if not pdf_file:
        raise HTTPException(status_code=400, detail="Aucun fichier PDF fourni.")

    try:
        course_content = extract_text_from_pdf(pdf_file.file)
        constraints_dict = json.loads(constraints)
        constraints_model = GenerationConstraints(**constraints_dict)

        exam_text = generate_exam(constraints_model.model_dump(), course_content)
        return {"epreuve_initiale": exam_text, "contenu_pdf": course_content}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Le champ constraints n'est pas un JSON valide.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de l'épreuve: {str(e)}")

@router.post("/personnaliser_epreuve/")
async def personnaliser_epreuve(
    modification_request: ModificationRequest = Body(...)
):
    """
    Personnalise une épreuve d'examen générée précédemment avec de nouvelles instructions en tenant compte du contenu PDF initial.
    """
    try:
        epreuve_modifiee = modify_exam(
            modification_request.epreuve_initiale,
            modification_request.nouveau_prompt,
            modification_request.contenu_pdf
        )
        return {"epreuve_personnalisee": epreuve_modifiee}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la personnalisation de l'épreuve: {str(e)}")