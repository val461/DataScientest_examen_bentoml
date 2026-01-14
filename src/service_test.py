# pytest-9.0.2

import requests, jwt, pytest
from src.service import check_token


@pytest.fixture
def login_url():
    return "http://127.0.0.1:3001/login"


@pytest.fixture
def predict_url():
    return "http://127.0.0.1:3001/predict"


@pytest.fixture
def valid_prediction_payload():
    return {
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


@pytest.fixture
def valid_login_payload():
    return {
        "credentials": {
            "username": "user123",
            "password": "password123"
        }
    }

@pytest.fixture
def wrong_login_payload():
    return {
        "credentials": {
            "username": "user123x",
            "password": "password123"
        }
    }

@pytest.fixture
def JWT_SECRET_KEY():
    return "your_jwt_secret_key_here"

@pytest.fixture
def JWT_ALGORITHM():
    return "HS256"

"""
Test de l'API de connexion :
    Vérifiez que l'API renvoie une erreur 401 pour des identifiants utilisateur incorrects.

Test de l'API de prédiction :
    Vérifiez que l'authentification réussit avec un jeton JWT valide.
    Vérifiez que l'authentification échoue si le jeton JWT a expiré.
    Vérifiez que l'API renvoie une prédiction valide pour des données d'entrée correctes.
    Vérifiez que l'API renvoie une erreur pour des données d'entrée invalides.
"""


def test_receive_valid_jwt(login_url, valid_login_payload, JWT_SECRET_KEY, JWT_ALGORITHM):
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=valid_login_payload
    )
    valid=True
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token","")
        token_validity = check_token(token)

        if token_validity=="expired":
            valid=False
        elif token_validity=="invalid":
            valid=False
        elif token_validity=="ok":
            pass
        else:
            raise ValueError
    else:
        valid=False
    assert valid


def test_wrong_credentials(login_url, wrong_login_payload):
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=wrong_login_payload
    )
    assert login_response.status_code == 401


def test_jwt_missing_or_invalid(predict_url, valid_prediction_payload):
    token = "invalid"
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=valid_prediction_payload
    )
    assert response.status_code==401

