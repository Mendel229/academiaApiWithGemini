from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Dict
import json
from app.ai.exam_generator import generate_exam
from app.models.generation import GenerationConstraints

router = APIRouter()

@router.post("/generer_epreuve/")
async def generer_epreuve(
    pdf_file: UploadFile = File(...),
    constraints: str = Form(...)
):
    """
    Génère une épreuve d'examen à partir d'un fichier PDF et de contraintes JSON envoyées en tant que chaîne.
    """
    if not pdf_file:
        raise HTTPException(status_code=400, detail="Aucun fichier PDF fourni.")

    try:
        constraints_dict = json.loads(constraints)
        constraints_model = GenerationConstraints(**constraints_dict)

        exam_text = generate_exam(constraints_model.model_dump(), pdf_file.file)
        return {"epreuve": exam_text}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Le champ constraints n'est pas un JSON valide.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de l'épreuve: {str(e)}")
