from ninja import NinjaAPI, Schema
from django.contrib.auth.models import User
from typing import Optional

apiv1 = NinjaAPI()

# Schema untuk input data registrasi
class Register(Schema):
    username: str
    password: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# Schema untuk output data pengguna
class UserOut(Schema):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

@apiv1.post('register/', response=UserOut)
def register(request, data: Register):
    """
    Endpoint untuk registrasi pengguna dengan validasi inputan:
    - username: minimal terdiri dari 5 karakter
    - password: minimal terdiri dari 8 karakter dan harus mengandung huruf dan angka
    """
    # Validasi panjang username
    if len(data.username) < 5:
        return apiv1.create_response(request, {"error": "Username harus terdiri dari minimal 5 karakter"}, status=400)

    # Validasi panjang password
    if len(data.password) < 8 or not any(char.isdigit() for char in data.password) or not any(char.isalpha() for char in data.password):
        return apiv1.create_response(request, {"error": "Password harus minimal 8 karakter dan mengandung huruf serta angka"}, status=400)

    # Membuat pengguna baru
    new_user = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
    )

    # Mengembalikan data pengguna baru
    return new_user
