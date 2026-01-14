import requests

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3001/login"
predict_url = "http://127.0.0.1:3001/predict"

# Données de connexion - must match the service signature
login_payload = {
    "credentials": {
        "username": "user123",
        "password": "password123"
    }
}

# Send a POST request to the login endpoint
login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=login_payload
)

# Check if the login was successful
if login_response.status_code == 200:
    token = login_response.json().get("token")
    print("Token JWT obtenu:", token)

    # Data to be sent to the prediction endpoint
    prediction_payload = {
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

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=prediction_payload
    )

    print("Réponse de l'API de prédiction:", response.text)
else:
    print("Erreur lors de la connexion:", login_response.text)

'''
curl -X POST http://127.0.0.1:3001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
        "gre": 320,
        "toefl": 110,
        "univ_rating": 4,
        "sop": 4.5,
        "lor": 4.0,
        "cgpa": 9.0,
        "research": 1
    }
  }'
'''
