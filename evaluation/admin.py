from django.contrib import admin
from .models import (
    Semester, Batch, Course, User, Module,
    CourseMaterial, Quiz, Question, QuizAttempt
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# ----------------------
# Custom User Admin
# ----------------------
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_approved', 'batch')
    list_filter = ('role', 'is_approved', 'batch')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'batch')}),
        ('Permissions', {'fields': ('role', 'is_approved', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'batch', 'password1', 'password2', 'is_approved')}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, UserAdmin)

# ----------------------
# Other Models
# ----------------------
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester')
    list_filter = ('semester',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name', 'semester', 'assigned_teacher')
    list_filter = ('semester', 'assigned_teacher')
    search_fields = ('course_code', 'name')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course',)
    search_fields = ('name',)

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('file', 'course', 'module', 'topic', 'uploaded_at')
    list_filter = ('course', 'module')
    search_fields = ('file', 'topic')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'status', 'start_time', 'end_time', 'duration', 'total_marks')
    list_filter = ('course', 'teacher', 'status')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'course', 'module', 'topic_tag', 'difficulty', 'marks', 'created_by')
    list_filter = ('course', 'module', 'difficulty', 'created_by')
    search_fields = ('question_text', 'topic_tag')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'student', 'score', 'started_at', 'submitted_at')
    list_filter = ('quiz', 'student')
    search_fields = ('quiz__title', 'student__username')
