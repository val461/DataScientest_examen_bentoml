# pytest-9.0.2

import requests, jwt, pytest
from src.service import check_token, create_jwt_token


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
def valid_jwt_token(login_url, valid_login_payload):
    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=valid_login_payload
    )
    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        if token is None:
            raise ValueError
        else:
            return token
    else:
        raise ValueError


def test_receive_valid_jwt(login_url, valid_login_payload):
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


def test_auth_with_valid_jwt(predict_url, valid_prediction_payload, valid_jwt_token):
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {valid_jwt_token}"
        },
        json=valid_prediction_payload
    )
    assert response.status_code==200


def test_expired_jwt(predict_url, valid_prediction_payload, valid_jwt_token):
    expired_token=create_jwt_token(user_id="user123", expiration_in_hours=-1)
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {expired_token}"
        },
        json=valid_prediction_payload
    )
    assert response.status_code==401


def test_predict_valid(predict_url, valid_prediction_payload, valid_jwt_token):
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {valid_jwt_token}"
        },
        json=valid_prediction_payload
    )
    valid=True
    if response.status_code==200:
        try:
            prediction = response.json()['prediction'][0][0]
        except Exception:
            valid=False
        if not isinstance(prediction, float):
            valid=False
    else:
        valid=False
    assert valid


def test_wrong_input_data(predict_url, valid_prediction_payload, valid_jwt_token):
    wrong_prediction_payload = {
        "input_data": {
            "gre": 320.1,
            "toefl": 110,
            "univ_rating": 4,
            "sop": 4.5,
            "lor": 4.0,
            "cgpa": 9.0,
            "research": 1
        }
    }
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {valid_jwt_token}"
        },
        json=wrong_prediction_payload
    )
    assert response.status_code!=200
