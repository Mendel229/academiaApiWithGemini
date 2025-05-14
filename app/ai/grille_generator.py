from app.ai.gemini_loader import load_gemini_model
import json

async def generer_grille(epreuve_text: str, prompt_grille: str = None) -> str:
    """
    Génère une grille de correction à partir du texte de l'épreuve,
    en utilisant éventuellement un prompt personnalisé.
    """
    model = load_gemini_model()
    prompt_base = f"""
Tu es un expert en génération d'épreuves techniques. 

À partir du texte d'épreuve brute fourni, reformate-le **strictement** selon ces règles :

### 🔧 Format OBLIGATOIRE :
```plaintext
epreuve_debut
  titre: Épreuve de [MATIÈRE] - [NIVEAU]
  duree: [DURÉE]
  exo_debut
    titre: [TITRE EXERCICE]
    type: QCM | code | ouverte
    consigne: null
    q_debut
      type: QCM | code | ouverte
      contenu: [ÉNONCÉ COMPLET]
      opt: a) [Option 1] (si QCM)
      opt: b) [Option 2]
      opt: c) [Option 3]
      opt: d) [Option 4]
    q_fin
    [autres questions...]
  exo_fin
  [autres exercices...]
epreuve_fin

grille_debut
  ex: 1 | q: 1 | type: QCM | rep: [a-d] | bareme: [POINTS]
  ex: 1 | q: 2 | type: code | attendu: [CRITÈRE 1] | bareme: [POINTS]
  ex: 1 | q: 2 | type: code | attendu: [CRITÈRE 2] | bareme: [POINTS]
  [autres réponses...]
grille_fin
📜 Texte source à convertir :
\"\"\"{epreuve_text}\"\"\"

⚠️ Règles IMPÉRATIVES :
Structure :

Titre exactement comme : Épreuve de [Matière] - [Niveau]

consigne: null si aucune consigne spécifique

Pour les QCM : 4 options obligatoires (a-d)

Questions de code :

Tout l'énoncé doit être dans contenu: (pas de balise code:)

Découper les attendus en sous-critères dans la grille (1 par ligne)

Grille de correction :

Barème total = 20 points

Pour les questions complexes : détailler les attendus (ex: "Constructeur fonctionnel", "Méthode afficherInfos()")

Toujours préciser type: (QCM/code/ouverte)

Balises INTERDITES :

Ne jamais utiliser code: dans les questions

Pas de texte hors balises

📌 Exemple de sortie VALIDE (extrait) :
q_debut
  type: code
  contenu: Créez une classe Rectangle avec attributs longueur/largeur...
q_fin

grille_debut
  ex: 1 | q: 1 | type: code | attendu: Attributs private corrects | bareme: 2
  ex: 1 | q: 1 | type: code | attendu: Constructeur initialisant les attributs | bareme: 2
grille_fin
❌ Ne pas inclure : commentaires, explications, ou texte hors balises.
"""   
    if prompt_grille:
        prompt_final = f"{prompt_base}\n\nInstructions supplémentaires du professeur : {prompt_grille}"
    else:
        prompt_final = prompt_base

    try:
        response = model.generate_content(prompt_final)
        grille_json_str = response.text
        # Tentative de parsing pour s'assurer que c'est un JSON valide (peut échouer si l'IA ne respecte pas parfaitement le format)
        grille_data = json.loads(grille_json_str)
        return grille_json_str
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON de la réponse de l'IA : {e}")
        print(f"Réponse brute de l'IA : {grille_json_str}")
        # En cas d'erreur de parsing, retourne la chaîne brute pour inspection
        return grille_json_str
    except Exception as e:
        raise Exception(f"Erreur lors de la génération de la grille: {str(e)}")