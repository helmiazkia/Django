from ninja import NinjaAPI, UploadedFile, File, Form
from ninja.responses import Response
from core.schema import CourseSchemaOut, CourseMemberOut, CourseSchemaIn
from core.schema import CourseContentMini, CourseContentFull
from core.schema import CourseCommentOut, CourseCommentIn
from core.models import Course, CourseMember, CourseContent, Comment
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja.pagination import paginate, PageNumberPagination
from django.http import Http404


from django.contrib.auth.models import User

apiv1 = NinjaAPI()
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

apiv1 = NinjaAPI(
    throttle=[
        AnonRateThrottle("1/s"),  # Contoh: 1 request/detik untuk pengguna anonim
        AuthRateThrottle("1/s"),  # Contoh: 1 requests/detik untuk pengguna terautentikasi
    ]
)
apiv1.add_router("/auth/", mobile_auth_router)

apiAuth = HttpJwtAuth()

@apiv1.get("/hello")
def hello(request):
    return "Hello World"

# - paginate list_courses
@apiv1.get("/courses", response=list[CourseSchemaOut])
@paginate(PageNumberPagination, page_size=3)
def list_courses(request):
    courses = Course.objects.select_related('teacher').all()
    return courses

# - my courses
@apiv1.get("/mycourses", auth=apiAuth, response=list[CourseMemberOut])
def my_courses(request):
    user = User.objects.get(id=request.user.id)
    courses = CourseMember.objects.select_related('user_id', 'course_id').filter(user_id=user)
    return courses

# - create course
@apiv1.post("/courses", auth=apiAuth, response={201:CourseSchemaOut})
def create_course(request, data: Form[CourseSchemaIn], image: UploadedFile = File(None)):
    user = User.objects.get(id=request.user.id)
    course = Course(
        name=data.name,
        description=data.description,
        price=data.price,
        image=image,
        teacher=user
    )

    if image:
        course.image.save(image.name, image)

    course.save()
    return 201, course

# - update course
@apiv1.post("/courses/{course_id}", auth=apiAuth, response=CourseSchemaOut)
def update_course(request, course_id: int, data: Form[CourseSchemaIn], image: UploadedFile = File(None)):
    if request.user.id != Course.objects.get(id=course_id).teacher.id:
        message = {"error": "Anda tidak diijinkan update course ini"}
        return Response(message, status=401)
    
    course = Course.objects.get(id=course_id)
    course.name = data.name
    course.description = data.description
    course.price = data.price
    if image:
        course.image.save(image.name, image)
    course.save()
    return course

# - detail course
@apiv1.get("/courses/{course_id}", response=CourseSchemaOut)
def detail_course(request, course_id: int):
    course = Course.objects.select_related('teacher').get(id=course_id)
    return course


# - list content course
@apiv1.get("/courses/{course_id}/contents", response=list[CourseContentMini])
def list_content_course(request, course_id: int):
    contents = CourseContent.objects.filter(course_id=course_id)
    return contents

# - detail content course
@apiv1.get("/courses/{course_id}/contents/{content_id}", response=CourseContentFull)
def detail_content_course(request, course_id: int, content_id: int):
    content = CourseContent.objects.get(id=content_id)
    return content

# - enroll course
@apiv1.post("/courses/{course_id}/enroll", auth=apiAuth, response=CourseMemberOut)
def enroll_course(request, course_id: int):
    user = User.objects.get(id=request.user.id)
    course = Course.objects.get(id=course_id)
    course_member = CourseMember(course_id=course, user_id=user, roles="std")
    course_member.save()
    # print(course_member)
    return course_member

@apiv1.get("/courses/{course_id}/contents/{content_id}", response=CourseContentFull)
def detail_content(request, course_id: int, content_id: int):
    try:
        course = Course.objects.get(id=course_id)
        content = CourseContent.objects.get(id=content_id, course_id=course)
    except (Course.DoesNotExist, CourseContent.DoesNotExist):
        raise Http404("Course or Content not found.")

    return content


@apiv1.post("/courses/{course_id}/contents", auth=apiAuth, response={201: CourseContentMini})
def create_content(request, course_id: int, name: str = Form(...), description: str = Form(...), video_url: str = Form(None), file_attachment: UploadedFile = File(None)):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise Http404(f"Course dengan ID {course_id} tidak ditemukan.")

    # Membuat konten baru untuk kursus
    content = CourseContent(
        name=name,
        description=description,
        video_url=video_url,
        file_attachment=file_attachment,
        course_id=course  # Menghubungkan dengan course_id, bukan detail lengkap
    )

    # Menyimpan file lampiran jika ada
    if file_attachment:
        content.file_attachment.save(file_attachment.name, file_attachment)

    # Menyimpan konten ke database
    content.save()

    # Mengembalikan konten dalam format CourseContentMini
    return 201, CourseContentMini.from_orm(content)


@apiv1.put("/courses/{course_id}/contents/{content_id}", auth=apiAuth, response=CourseContentMini)
def update_content(request, course_id: int, content_id: int, name: str = Form(...), description: str = Form(...), video_url: str = Form(None), file_attachment: UploadedFile = File(None), is_deleted: bool = Form(False)):
    try:
        course = Course.objects.get(id=course_id)
        content = CourseContent.objects.get(id=content_id, course_id=course)
    except (Course.DoesNotExist, CourseContent.DoesNotExist):
        raise Http404("Course or Content not found.")

    content.name = name
    content.description = description
    content.video_url = video_url
    content.is_deleted = is_deleted
    
    if file_attachment:
        content.file_attachment.save(file_attachment.name, file_attachment)

    content.save()

    return content

@apiv1.delete("/courses/{course_id}/contents/{content_id}", auth=apiAuth)
def delete_content(request, course_id: int, content_id: int):
    try:
        course = Course.objects.get(id=course_id)
        content = CourseContent.objects.get(id=content_id, course_id=course)
    except (Course.DoesNotExist, CourseContent.DoesNotExist):
        raise Http404("Course or Content not found.")

    content.delete()
    
    return {"message": "Content deleted successfully"}


# - list content comment
@apiv1.get("/contents/{content_id}/comments", auth=apiAuth, response=list[CourseCommentOut])
def list_content_comment(request, content_id: int):
    comments = Comment.objects.filter(content_id=content_id).select_related('member_id', 'member_id__user_id')
    return comments


# - create content comment
# - create content comment
@apiv1.post("/contents/{content_id}/comments", auth=apiAuth, response={201: CourseCommentOut})
def create_content_comment(request, content_id: int, data: CourseCommentIn):
    try:
        content = CourseContent.objects.get(id=content_id)
    except CourseContent.DoesNotExist:
        raise Http404(f"Content with id {content_id} not found")

    user = request.user
    if not content.course_id.is_member(user):
        return Response({"error": "You are not authorized to create a comment in this content"}, status=401)
    
    # Gunakan filter() dan first() untuk menangani kemungkinan ada lebih dari satu CourseMember
    member = CourseMember.objects.filter(course_id=content.course_id, user_id=user).first()
    
    if not member:
        return Response({"error": "You are not enrolled in this course"}, status=404)
    
    comment = Comment(content_id=content, member_id=member, comment=data.comment)
    comment.save()
    return 201, comment

# - delete content comment
@apiv1.delete("/contents/{content_id}/comments", auth=apiAuth)
def delete_comment_by_content(request, content_id: int):
    # Cari komentar terkait dengan content_id dan dibuat oleh pengguna yang sedang login
    comments = Comment.objects.filter(
        content_id=content_id, 
        member_id__user_id=request.user
    )

    # Periksa apakah pengguna adalah instruktur atau admin kursus
    is_instructor = Course.objects.filter(
        id=content_id, 
        teacher_id=request.user.id
    ).exists()

    if not comments.exists() and not is_instructor:
        return Response({"error": "Comment not found or you do not have permission to delete this comment"}, status=404)

    # Jika pengguna adalah instruktur, hapus semua komentar terkait content_id
    if is_instructor:
        deleted_count, _ = Comment.objects.filter(content_id=content_id).delete()
        return {"message": f"Deleted {deleted_count} comment(s) successfully"}
    
    # Jika pengguna hanya pembuat komentar, hapus komentarnya saja
    deleted_count, _ = comments.delete()

    if deleted_count > 0:
        return {"message": "Comment(s) deleted successfully"}
    else:
        return Response({"error": "No comments were deleted"}, status=404)
