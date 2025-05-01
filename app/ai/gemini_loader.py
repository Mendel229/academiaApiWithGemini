import google.generativeai as genai
from decouple import config

def load_gemini_model(model_name="gemini-2.0-flash"):

    genai.configure(api_key=config("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model_name)
    return model

# test rapide
if __name__ == "__main__":
    model = load_gemini_model()
    print(f"Modèle Gemini chargé: {model.name}")