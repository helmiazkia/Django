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
        AnonRateThrottle("1/s"),  # Contoh: 10 requests/detik untuk pengguna anonim
        AuthRateThrottle("1/s"),  # Contoh: 100 requests/detik untuk pengguna terautentikasi
    ]
)
apiv1.add_router("/auth/", mobile_auth_router)

apiAuth = HttpJwtAuth()

@apiv1.get("/hello")
def hello(request):
    return "Hello World"

# - paginate list_courses
@apiv1.get("/courses", response=list[CourseSchemaOut])
@paginate(PageNumberPagination, page_size=1)
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
# - delete content comment
@apiv1.delete("/contents/{content_id}/comments", auth=apiAuth)
def delete_comment_by_content(request, content_id: int):
    # Cari komentar yang terkait dengan content_id dan user yang sedang login
    comments = Comment.objects.filter(content_id=content_id, member_id__user_id=request.user)
    
    if not comments.exists():
        return Response({"error": "Comment not found for the given content and user"}, status=404)
    
    # Hapus semua komentar yang ditemukan
    deleted_count, _ = comments.delete()
    
    if deleted_count > 0:
        return {"message": "Comment(s) deleted successfully"}
    else:
        return Response({"error": "No comments were deleted"}, status=404)
