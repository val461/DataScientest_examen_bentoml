import bentoml
import numpy as np
from pydantic import BaseModel
from starlette.responses import JSONResponse
import jwt
from datetime import datetime, timedelta

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

# User credentials for authentication
USERS = {
    "user123": "password123",
    "user456": "password456"
}


# Pydantic model to validate input data
class InputModel(BaseModel):
    gre: int
    toefl: int
    univ_rating: int
    sop: float
    lor: float
    cgpa: float
    research: int


def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def check_token(token):
    try:
        # On gère le cas "Bearer <token>" ou juste "<token>"
        parts = token.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token_val = parts[1]
        else:
            token_val = token

        jwt.decode(token_val, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"
    return "ok"

@bentoml.service
class ModelService:
    def __init__(self) -> None:
        # Load the model using bentoml sklearn API
        self.model = bentoml.sklearn.load_model("admission_model:latest")

    # Login endpoint
    @bentoml.api
    def login(self, credentials: dict) -> dict:
        username = credentials.get("username")
        password = credentials.get("password")

        if username in USERS and USERS[username] == password:
            token = create_jwt_token(username)
            return {"token": token}
        else:
            return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    # Prediction endpoint
    @bentoml.api
    def predict(self, input_data: InputModel, ctx: bentoml.Context = None) -> dict:
        request = ctx.request
        token = request.headers.get("Authorization")

        if not token:
            ctx.response.status_code = 401
            return {"detail": "Missing authentication token"}

        token_validity = check_token(token)
        if token_validity=="expired":
            ctx.response.status_code = 401
            return {"detail": "Token has expired"}
        elif token_validity=="invalid":
            ctx.response.status_code = 401
            return {"detail": "Invalid token"}
        elif token_validity=="ok":
            pass
        else:
            raise ValueError

        # Convert the input data to a numpy array
        input_series = np.array([
            input_data.gre,
            input_data.toefl,
            input_data.univ_rating,
            input_data.sop,
            input_data.lor,
            input_data.cgpa,
            input_data.research
        ])

        # Run prediction
        result = self.model.predict(input_series.reshape(1, -1))

        return {
            "prediction": result.tolist()
        }

# bentoml serve src.service:ModelService --port 3001
