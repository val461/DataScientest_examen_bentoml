import bentoml
import numpy as np
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
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


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response


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


@bentoml.service(
    middlewares=[JWTAuthMiddleware]
)
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
    def predict(self, input_data: InputModel) -> dict:
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
