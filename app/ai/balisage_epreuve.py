from app.ai.gemini_loader import load_gemini_model

async def baliser_epreuve(texte_epreuve: str) -> dict:
    """
    Analyse le texte de l'épreuve avec l'IA et le balise directement
    dans le format requis pour l'enregistrement, incluant le type 'code'.
    Retourne un dictionnaire contenant le texte balisé de l'épreuve.
    """
    model = load_gemini_model()

    prompt = f"""Tu es un expert en pédagogie universitaire. Analyse le texte de l'épreuve suivant et balise-le **exactement** selon le format ci-dessous pour faciliter l'enregistrement dans une base de données.

    ---

    Texte de l'épreuve :
    \"\"\"{texte_epreuve}\"\"\"

    ---

    ## Format de sortie attendu :

    ```
    epreuve_debut
      titre: Titre de l'épreuve (si identifiable)
      duree: Durée (si identifiable)
      exo_debut
        titre: Titre de l'exercice (si identifiable)
        type: QCM | ouverte | code
        consigne: Consigne de l'exercice (si présente)
        q_debut
          type: QCM | ouverte | code
          contenu: Texte de la question
          opt: Option a) ... (si QCM)
          opt: Option b) ... (si QCM)
          ...
          code: // Zone de code à compléter (si type est code)
        q_fin
        q_debut
          type: ouverte
          contenu: Texte de la question
        q_fin
        q_debut
          type: code
          contenu: Description de la tâche de codage
          code_initial: Code initial fourni (si applicable)
        q_fin
      exo_fin
      ... (autres exercices) ...
    epreuve_fin
    grille_debut
      ex: Numéro de l'exercice | q: Numéro de la question | type: QCM | rep: Lettre de la réponse correcte | bareme: Nombre de points
      ex: Numéro de l'exercice | q: Numéro de la question | type: ouverte | attendu: Indications de la réponse attendue | bareme: Nombre de points
      ex: Numéro de l'exercice | q: Numéro de la question | type: code | attendu: Description du code attendu (fonctionnalité, logique) | bareme: Nombre de points
      ...
    grille_fin
    ```

    ---

    **Consignes importantes :**

    - **Respecte scrupuleusement** le format de balisage ci-dessus.
    - Essaie d'identifier et d'inclure le titre et la durée de l'épreuve si présents.
    - Structure l'épreuve en exercices et en questions si possible.
    - Indique le type de chaque question (`QCM`, `ouverte` ou `code`).
    - Pour les QCM, inclus toutes les options avec la balise `opt`.
    - Pour les questions de type `code`, utilise la balise `code` pour indiquer l'endroit où le code doit être écrit dans l'énoncé de la question, et potentiellement une balise `code_initial` si du code de départ est fourni.
    - Génère la grille de correction en indiquant l'exercice, la question, le type, la réponse correcte (pour les QCM), les indications de la réponse attendue (pour les questions ouvertes et de code), et le barème.
    - **N'ajoute aucun texte d'introduction ou de conclusion.**
    - Si certaines informations ne sont pas clairement identifiables, ne les inclus pas.
    - Si la grille de correction ne contient pas de bareme tu peux uniquement dans ce cas ajouter le bareme:
      Ne répartis pas les points exercice par exercice, mais bien sur l’ensemble des questions de l’épreuve

      Évite autant que possible les décimales «complexes» (ex. 2,33 ou 4,17).

      Tu peux utiliser uniquement des fractions en quart de point pour plus de précision :

          0,25 point (¼),

          0,50 point (½),

          0,75 point (¾).

      L’objectif est de conserver un barème clair, équilibré et pédagogique, tout en respectant strictement le total de 20 points

    Résultat balisé :
    """

    try:
        response = model.generate_content(prompt)
        texte_balise = response.text
        return {"epreuve_balisee": texte_balise}
    except Exception as e:
        raise Exception(f"Erreur lors de l'analyse et du balisage de l'épreuve par l'IA: {str(e)}")