from django.contrib import admin
from core.models import Course, Comment, CourseContent

# Admin untuk model Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description", "teacher", 'created_at']
    list_filter = ["teacher"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    fields = ["name", "description", "price", "image", "teacher", "created_at", "updated_at"]

# Admin untuk model Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'content_id', 'comment', 'created_at']
    list_filter = ['member_id', 'content_id']
    search_fields = ['comment']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['content_id', 'member_id', 'comment', 'created_at', 'updated_at']

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ["name", "course_id", "created_at"]
    list_filter = ["course_id"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    fields = ["name", "description", "course_id", "video_url", "file_attachment", "created_at", "updated_at"]
