from ninja import NinjaAPI
from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from pydantic import BaseModel
from django.http import JsonResponse

# Inisialisasi API
api = NinjaAPI()

# Model untuk login input
class LoginSchema(BaseModel):
    username: str
    password: str

# Login endpoint
@api.post("/auth/login")
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return JsonResponse({"detail": "Invalid credentials"}, status=401)

    # Buat token JWT
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username,
        "user_id": user.id,
    }

# Refresh token endpoint
@api.post("/auth/refresh")
def refresh_token(request, token: str):
    try:
        refresh = RefreshToken(token)
        return {"access": str(refresh.access_token)}
    except Exception:
        return JsonResponse({"detail": "Invalid token"}, status=401)

# Protected route (contoh endpoint)
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            return jwt_authenticator.get_user(validated_token)
        except Exception:
            return None

@api.get("/protected", auth=AuthBearer())
def protected_route(request):
    return {"message": f"Hello, {request.auth.username}!"}
