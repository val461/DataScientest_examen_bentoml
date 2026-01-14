# pytest-9.0.2

import requests

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3001/login"
predict_url = "http://127.0.0.1:3001/predict"

"""
Test de l'authentification JWT :
    Vérifiez que l'authentification échoue si le jeton JWT est manquant ou invalide.
    Vérifiez que l'authentification échoue si le jeton JWT a expiré.
    Vérifiez que l'authentification réussit avec un jeton JWT valide.

Test de l'API de connexion :
    Vérifiez que l'API renvoie un jeton JWT valide pour des identifiants utilisateur corrects.
    Vérifiez que l'API renvoie une erreur 401 pour des identifiants utilisateur incorrects.

Test de l'API de prédiction :
    Vérifiez que l'API renvoie une erreur 401 si le jeton JWT est manquant ou invalide.
    Vérifiez que l'API renvoie une prédiction valide pour des données d'entrée correctes.
    Vérifiez que l'API renvoie une erreur pour des données d'entrée invalides.
"""

# Data to be sent to the prediction endpoint
valid_prediction_payload = {
    "input_data": {
        "gre": 320,
        "toefl": 110,
        "univ_rating": 4,
        "sop": 4.5,
        "lor": 4.0,
        "cgpa": 9.0,
        "research": 1
    }
}


def test_jwt_missing_or_invalid():
    token = "invalid"
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=valid_prediction_payload
    )
    print("Réponse de l'API de prédiction:", response.text)
    #FIXME
    assert False
