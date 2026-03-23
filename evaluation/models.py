from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

# ----------------------
# Step 1: Semester
# ----------------------
class Semester(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


# ----------------------
# Step 2: Batch
# ----------------------
class Batch(models.Model):
    name = models.CharField(max_length=50)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.semester.name})"


# ----------------------
# Step 3: Course
# ----------------------
class Course(models.Model):
    course_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_enrolled', blank=True)
    assigned_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'Teacher'},
        null=True,
        blank=True,
        on_delete=models.SET_NULL   # ✅ persists if teacher deleted
    )

    class Meta:
        unique_together = ('course_code', 'semester')

    def __str__(self):
        return f"{self.course_code} - {self.name} ({self.semester.name})"


# ----------------------
# Step 4: Custom User
# ----------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ("Student", "Student"),
        ("Teacher", "Teacher"),
        ("Admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)
    batch = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.SET_NULL)


# ----------------------
# Step 5: Module
# ----------------------
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('course', 'name')

    def __str__(self):
        return f"{self.course.name} - {self.name}"


# ----------------------
# Step 6: Course Materials
# ----------------------
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    module = models.ForeignKey(Module, null=True, blank=True, on_delete=models.SET_NULL, related_name="materials")
    topic = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(   # ✅ persists if teacher deleted
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="uploaded_materials"
    )

    def __str__(self):
        return f"{self.course.name} - {self.file.name}"

    def clean(self):
        if self.module and self.module.course != self.course:
            raise ValidationError("Selected module does not belong to this course.")


# ----------------------
# Step 7: Quiz
# ----------------------
class Quiz(models.Model):
    STATUS_CHOICES = (
        ("Draft", "Draft"),
        ("Published", "Published"),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    module = models.ForeignKey(Module, null=True, blank=True, on_delete=models.SET_NULL, related_name="quizzes")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'Teacher'},
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=100, blank=True, null=True)

    # Scheduling
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(
        help_text="Time in minutes", null=True, blank=True
    )

    # Marks
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    marks_per_question = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="If set, applies same mark to all questions"
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Draft")
    batches = models.ManyToManyField(Batch, blank=True, related_name="quizzes")

    # ✅ Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"


# ----------------------
# Step 8: Question
# ----------------------
class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        null=True,
        blank=True
    )
    module = models.ForeignKey(Module, null=True, blank=True, on_delete=models.SET_NULL)
    topic_tag = models.CharField(max_length=100, blank=True)

    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_ans = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="Medium")
    marks = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    created_by = models.ForeignKey(   # ✅ persists if teacher deleted
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'Teacher'},
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_ai_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question_text[:50]}..."


# ----------------------
# Step 9: Quiz Attempt
# ----------------------
class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'Student'},
        on_delete=models.CASCADE
    )
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"

class QuizAnswer(models.Model):
    attempt = models.ForeignKey("QuizAttempt", on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')], null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attempt.student.username} - {self.question.id} - {self.selected_option}"
