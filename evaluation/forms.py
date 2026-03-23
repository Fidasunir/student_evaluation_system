from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Batch

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Batch
import re

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        initial="Teacher"
    )
    batch = forms.ModelChoiceField(
        queryset=Batch.objects.all(),
        required=False,
        empty_label="Select batch"
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "role",
            "batch"
        ]

def clean(self):
    cleaned_data = super().clean()
    role = cleaned_data.get("role")
    batch = cleaned_data.get("batch")
    username = cleaned_data.get("username")

    # Teachers should not have a batch
    if role == "Teacher" and batch:
        self.add_error("batch", "Teachers should not be assigned a batch.")

    # Students must have a batch
    if role == "Student" and not batch:
        self.add_error("batch", "Students must be assigned to a batch.")

    # ✅ Enforce username format for Students
    if role == "Student" and username:
        pattern = r"^\d{2}[A-Za-z]+$"
        if not re.match(pattern, username):
            self.add_error(
                "username",
                "Username must be in the format: batch year + name (e.g., 25fida)"
            )

    return cleaned_data



from django import forms
from .models import Quiz, CourseMaterial

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'module', 'topic', 'status', 'start_time', 'end_time', 'duration', 'batches']




from django import forms
from .models import Quiz

# Form for Draft Quiz (no batch selection)
class DraftQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'module', 'topic']  # Exclude batches

# Form for Publishing (requires batch selection)
class PublishQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'module', 'topic', 'batches']
        widgets = {
            'batches': forms.CheckboxSelectMultiple(),  # Optional UI enhancement
        }

from django import forms
from .models import Module

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Module Name'}),
        }

from django import forms
from .models import CourseMaterial

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['module', 'topic', 'file']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional topic'}),
            'module': forms.Select(attrs={'class': 'form-select'}),
        }
