# core/views.py

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.db.models import Max, Min, Avg, Count
from .models import Course  # Pastikan model Course sudah diimport

# Fungsi untuk pengujian
def testing(request):
    user_test = User.objects.filter(username="usertesting")
    if not user_test.exists():
        user_test = User.objects.create_user(
            username="usertesting", 
            email="usertest@email.com", 
            password="sanditesting"
        )
    all_users = serializers.serialize('python', User.objects.all())

    admin = User.objects.get(pk=1)
    user_test.delete()

    after_delete = serializers.serialize('python', User.objects.all())

    response = {
        "admin_user": serializers.serialize('python', [admin])[0],
        "all_users": all_users,
        "after_del": after_delete,
    }
    return JsonResponse(response)

# Fungsi untuk mendapatkan semua course
def allCourse(request):
    all_courses = Course.objects.all()
    result = []
    for course in all_courses:
        record = {
            'id': course.id, 
            'name': course.name,
            'description': course.description,
            'price': course.price,
            'teacher': {
                'id': course.teacher.id,
                'username': course.teacher.username,
                'email': course.teacher.email,
                'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
            }
        }
        result.append(record)
    return JsonResponse(result, safe=False)

# Fungsi untuk mendapatkan course yang dibuat oleh user tertentu
def userCourses(request):
    user = User.objects.get(pk=3)
    courses = Course.objects.filter(teacher=user.id)
    
    course_data = []
    for course in courses:
        record = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'price': course.price
        }
        course_data.append(record)
    
    result = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'fullname': f"{user.first_name} {user.last_name}",
        'courses': course_data
    }
    return JsonResponse(result, safe=False)

# Fungsi untuk mendapatkan statistik dari semua course
def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    result = {
        'course_count': courses.count(),
        'stats': stats
    }
    return JsonResponse(result, safe=False)

# Fungsi untuk mendapatkan statistik course yang memiliki kata "python" di deskripsi
def courseMemberStat(request):
    courses = Course.objects.filter(description__contains='python') \
                            .annotate(member_num=Count('coursemember'))
    
    course_data = []
    for course in courses:
        record = {
            'id': course.id,
            'name': course.name,
            'price': course.price,
            'member_count': course.member_num
        }
        course_data.append(record)
    
    result = {
        'data_count': len(course_data),
        'data': course_data
    }
    return JsonResponse(result, safe=False)


