"""
URL configuration for simplelms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static


# simplelms/urls.py
from core import views
from core.api import api  # Import Ninja API


urlpatterns = [
    path('admin/', admin.site.urls),
    path('testing/', views.testing, name='testing'),
    path('all_courses/', views.allCourse, name='all_courses'),
    path('user_courses/', views.userCourses, name='user_courses'),
    path('course_stats/', views.courseStat, name='course_stats'),
    path('course_member_stats/', views.courseMemberStat, name='course_member_stats'),
    path('silk/', include('silk.urls', namespace='silk')),
    path('course-statistics/', views.courseStat, name='course_statistics'),
    path("api/", api.urls),  # Tambahkan ini untuk endpoint API
    

]
