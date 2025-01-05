from datetime import datetime
from ninja import Schema

class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str

class CourseSchema(Schema):
    id: int
    name: str
    description: str
    price: int
    teacher: UserSchema
    created_at: datetime  # Tetap datetime
    updated_at: datetime  # Tetap datetime
    is_deleted: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Serialize datetime ke ISO 8601
        }

class CourseCreateSchema(Schema):
    name: str
    description: str
    price: int
    teacher_id: int  # Mengacu pada User ID

class CourseUpdateSchema(Schema):
    name: str = None
    description: str = None
    price: int = None
