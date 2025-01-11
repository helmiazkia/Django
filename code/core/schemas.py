from pydantic import BaseModel, Field
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime



# Skema untuk Course
class CourseSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int
    teacher: Optional[dict]  # Representasi informasi guru

    class Config:
        orm_mode = True


# Skema untuk CourseMember

class CourseMemberSchema(BaseModel):
    course_id: int
    user_id: int
    roles: str
    created_at: datetime
    updated_at: datetime



# Skema untuk CourseStatistics
class CourseStatisticsSchema(BaseModel):
    course_count: int
    max_price: float
    min_price: float
    avg_price: float
