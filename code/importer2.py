import os
import sys
import django
import csv

# Menentukan path untuk settings Django
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'

# Inisialisasi Django
django.setup()

# Import model dari Django
from django.contrib.auth.models import User
from core.models import Course, CourseMember

# Fungsi untuk mengimpor data user dari CSV
def import_users():
    with open('./csv_data/user-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for num, row in enumerate(reader):
            if not User.objects.filter(username=row['username']).exists():
                User.objects.create_user(
                    id=num+2,
                    username=row['username'], 
                    password=row['password'], 
                    email=row['email']
                )

# Fungsi untuk mengimpor data course dari CSV
def import_courses():
    with open('./csv_data/course-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for num, row in enumerate(reader):           
            if not Course.objects.filter(pk=num+1).exists():                        
                Course.objects.create(
                    id=num+1, 
                    name=row['name'], 
                    description=row['description'], 
                    price=row['price'],
                    teacher=User.objects.get(pk=int(row['teacher']))
                )

# Fungsi untuk mengimpor data course member dari CSV
def import_course_members():
    with open('./csv_data/member-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for num, row in enumerate(reader):
            if not CourseMember.objects.filter(pk=num+1).exists():
                CourseMember.objects.create(
                    course_id=Course.objects.get(pk=int(row['course_id'])),
                    user_id=User.objects.get(pk=int(row['user_id'])),
                    id=num+1,
                    roles=row['roles']
                )

# Menjalankan fungsi-fungsi impor
if __name__ == '__main__':
    import_users()
    import_courses()
    import_course_members()
    print("Data berhasil diimpor dari CSV.")
