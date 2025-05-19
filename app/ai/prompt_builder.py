def build_prompt_from_constraints(course_content: str, constraints: dict) -> str:
    """
    Construit un prompt pour le modèle Gemini à partir du contenu du cours et des contraintes.
    """
    matiere = constraints.get("matiere", "matière inconnue")
    niveau = constraints.get("niveau", "niveau inconnu")
    duree = constraints.get("duree", "non spécifiée")
    nb_exo = constraints.get("Nombre d'exercice", "non précisé")
    objectifs = "\n- ".join(constraints.get("objectifs", []))
    custom_prompt = constraints.get("prompt", "")

    prompt = f"""
    Tu es un expert en pédagogie universitaire. 
    À partir du document de cours ci-dessous, 
    génère une **épreuve complète** avec une **grille de correction**,
    en respectant **strictement** le format balisé ci-dessous.
    ---📘 Matière : {matiere}  🎓 Niveau : {niveau}  ⏳ Durée : {duree}  
    📄 Nombre d’exercices souhaité : {nb_exo}  🎯 Objectifs pédagogiques :  - {objectifs}  
    🛠️ Contraintes spécifiques à respecter IMPÉRATIVEMENT :  {custom_prompt}  
    ➡️ ⚠️ Tu dois respecter à la lettre ces consignes :  
    - Ne modifie pas le nombre d’exercices ni le type de questions.  
    - Génère exactement le nombre de QCM, de questions ouvertes et de questions de code demandées.  
    - Ne regroupe pas les questions ou les transforme.
    - Le **barème total doit faire 20 points**. Quelle que soit la structure de l’épreuve (nombre d’exercices, nombre de questions par exercice), la somme des points de toutes les questions de l’épreuve doit impérativement être exactement 20 points.

Ne répartis pas les points exercice par exercice, mais bien sur l’ensemble des questions de l’épreuve.

Évite autant que possible les décimales «complexes» (ex. 2,33 ou 4,17).

Tu peux utiliser uniquement des fractions en quart de point pour plus de précision :

    0,25 point (¼),

    0,50 point (½),

    0,75 point (¾).

L’objectif est de conserver un barème clair, équilibré et pédagogique, tout en respectant strictement le total de 20 points       
    - Si aucune répartition spécifique n’est mentionnée dans le prompt du professeur, répartis les 20 points équitablement entre le totals des questions de l'épreuve.       
    - Sinon, suis **strictement** les consignes données par le professeur dans la partie "prompt".---
    Cours :\"\"\"{course_content}\"\"\"---## Format de sortie attendu :epreuve_debut  titre: Épreuve de {matiere} - {niveau}  duree: {duree}  exo_debut  titre: ...  type: QCM | ouverte | code  consigne: ...  q_debut  type: QCM | ouverte | code  contenu: ...  opt: ...  opt: ...  opt: ... (si QCM)  code: ... (si code)  q_fin  q_debut  type: ouverte  contenu: ...  q_fin  q_debut  type: code  contenu: ...  code: ...  attendu: ... (pour le code)  q_fin  exo_fin  ... (autres exercices) ...epreuve_fin  grille_debut  ex: 1 | q: 1 | type: QCM | rep: a | bareme: 1  ex: 1 | q: 2 | type: ouverte | attendu: bonne définition + exemple | bareme: 4  ex: 2 | q: 1 | type: code | attendu: code python fonction ... | bareme: 5  grille_fin  ---### ⛔ Contraintes techniques supplémentaires :- N’inclus aucun texte d’introduction ou de conclusion.  - **Respecte strictement** les balises suivantes :    `epreuve_debut`, `epreuve_fin`,    `exo_debut`, `exo_fin`,    `q_debut`, `q_fin`,    `type`, `contenu`, `opt`, `rep`, `bareme`, `attendu`, `code`, etc.  - Si une question est de type QCM, utilise les balises `opt` pour chaque option.  - Si une question est de type `code`, utilise la balise `code` pour l'énoncé du code à écrire et `attendu` pour la description du code attendu dans la grille.  - Toutes les réponses attendues et barèmes doivent être dans la **grille_debut** / **grille_fin**.---Ce format est requis pour pouvoir enregistrer automatiquement les données dans une base de données."""
    
    return prompt