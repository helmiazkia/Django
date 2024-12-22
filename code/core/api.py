from ninja import NinjaAPI
from core.models import Course, CourseMember
from core.schemas import CourseSchema, CourseMemberSchema, CourseStatisticsSchema
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg
from typing import List

api = NinjaAPI()


@api.get('/courses', response=List[CourseSchema])
def get_courses(request):
    courses = Course.objects.all()  # Ambil semua data dari model Course
    return [CourseSchema(
        id=course.id,
        name=course.name,
        description=course.description,
        price=course.price,
        teacher={
            "id": course.teacher.id,
            "username": course.teacher.username,
            "email": course.teacher.email,
            "fullname": f"{course.teacher.first_name} {course.teacher.last_name}"
        }
    ) for course in courses]  # Konversi setiap objek model ke skema



@api.get('/courses/{course_id}', response=CourseSchema)
def get_course(request, course_id: int):
    course = Course.objects.get(id=course_id)
    return CourseSchema(**{
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "price": course.price,
        "teacher": {
            "id": course.teacher.id,
            "username": course.teacher.username,
            "email": course.teacher.email,
            "fullname": f"{course.teacher.first_name} {course.teacher.last_name}",
        },
    })



@api.get("/course-statistics", response=CourseStatisticsSchema)
def get_course_statistics(request):
    stats = Course.objects.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    return {
        "course_count": Course.objects.count(),
        "max_price": stats["max_price"],
        "min_price": stats["min_price"],
        "avg_price": stats["avg_price"],
    }


@api.get('/course-members', response=List[CourseMemberSchema])
def get_course_members(request):
    members = CourseMember.objects.all()  # Ambil data dari model
    return [
        CourseMemberSchema(
            course_id=member.course_id.id,
            user_id=member.user_id.id,
            roles=member.roles,
            created_at=member.created_at,
            updated_at=member.updated_at
        )
        for member in members  # Konversi setiap objek model ke skema
    ]
