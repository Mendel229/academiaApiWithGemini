from fastapi import FastAPI
from app.api import epreuves, questions, bonnes_reponses, generer_epreuve, save_epreuve, grille_epreuve, analyser_epgrille
from app.models import relationships
from app.models.base import Base

app = FastAPI()

app.include_router(epreuves.router)
app.include_router(questions.router)
app.include_router(bonnes_reponses.router)
app.include_router(generer_epreuve.router)
app.include_router(save_epreuve.router)
app.include_router(grille_epreuve.router)
app.include_router(analyser_epgrille.router)

@app.get("/")
async def kwabo() :
    return {"message": "Bienvenue sur l'API de composition en ligne!"}