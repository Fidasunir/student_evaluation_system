from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ----------------- Home -----------------
    path("", views.index, name="index"),

    # ----------------- Auth -----------------
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password-reset-simple/", views.simple_password_reset, name="simple_password_reset"),

    # ----------------- Dashboards -----------------
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # ----------------- Teacher Management -----------------
    path("approve_teachers/", views.approve_teachers, name="approve_teachers"),
    path("manage_teachers/", views.manage_teachers, name="manage_teachers"),

    # ----------------- Semester Management -----------------
    path("manage_semesters/", views.manage_semesters, name="manage_semesters"),

    # ----------------- Batch Management -----------------
    path("manage_batches/", views.manage_batches, name="manage_batches"),

    # ----------------- Course Management -----------------
    path("manage_courses/", views.manage_courses, name="manage_courses"),


  path('teacher_analytics/', views.teacher_analytics, name='teacher_analytics'),
  path('quiz/<int:quiz_id>/analytics/', views.quiz_analytics, name='quiz_analytics'),


    # ----------------- Module Detail / Repository -----------------
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/module/create/', views.create_module, name='create_module'),
    path('course/<int:course_id>/module/<int:module_id>/', views.module_detail, name='module_detail'),
    path("courses/<int:course_id>/modules/<int:module_id>/edit/", views.edit_module, name="edit_module"),
    path('course/<int:course_id>/module/<int:module_id>/delete/', views.delete_module, name='delete_module'),

    # ----------------- Course Material -----------------
    path('material/delete/<int:material_id>/', views.delete_material, name='delete_material'),

    # ----------------- Question Management -----------------
    path('questions/create_quiz/', views.create_quiz_from_questions, name='create_quiz_from_questions'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('question/<int:question_id>/add-to-quiz/', views.add_to_quiz, name='add_to_quiz'),

    # ----------------- Quiz Management -----------------
    # Specific quiz URLs first
    path('quiz/<int:quiz_id>/attempts/', views.quiz_attempts, name='quiz_attempts'),
    path('quiz/<int:quiz_id>/view/', views.view_quiz, name='view_quiz'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('quiz/<int:quiz_id>/publish/', views.publish_quiz, name='publish_quiz'),
    path('quiz/<int:quiz_id>/republish/', views.republish_quiz, name='republish_quiz'),

    # Quiz attempt & submission
    path('quiz/attempt/<int:quiz_id>/', views.attempt_quiz, name='attempt_quiz'),
    path('quiz/submit/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),

    # Quiz result
    path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
   path('student/results/', views.student_results, name='student_results'),
  path("attempt/<int:attempt_id>/details/json/", views.attempt_details_json, name="attempt_details_json"),



    # General catch-all (always last)
    path('quiz/<int:quiz_id>/', views.quiz_detail, name="quiz_detail"),

    path("analytics/", views.analytics_dashboard, name="analytics_dashboard"),

]

# ----------------- Serve media in debug -----------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
