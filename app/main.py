from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import epreuves, questions, bonnes_reponses, generer_epreuve, save_epreuve, grille_epreuve, analyser_epgrille, copies, reponse_eleve, correction_copie, save_epreuve_baliser, filiere, matiere, option_etude, enseignement, session_examen, affectation_epreuve

from app.models import relationships
from app.models.base import Base

app = FastAPI()

# =================================================================
# Configurez le middleware CORS ici
# =================================================================
origins = [
    "http://localhost:4200",
    #"https://votre-frontend-angular.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =================================================================
# Fin de la configuration CORS
# =================================================================

app.include_router(epreuves.router)
app.include_router(questions.router)
app.include_router(bonnes_reponses.router)
app.include_router(generer_epreuve.router)
app.include_router(save_epreuve.router)
app.include_router(save_epreuve_baliser.router)
app.include_router(grille_epreuve.router)
app.include_router(analyser_epgrille.router)
app.include_router(copies.router)
app.include_router(reponse_eleve.router)
app.include_router(correction_copie.router)
app.include_router(filiere.router)
app.include_router(matiere.router)
app.include_router(option_etude.router)
app.include_router(enseignement.router)
app.include_router(session_examen.router)
app.include_router(affectation_epreuve.router)


@app.get("/")
async def kwabo() :
    return {"message": "Bienvenue sur l'API de composition en ligne!"}
