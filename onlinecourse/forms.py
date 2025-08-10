from django import forms
from .models import Lesson, Question

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "order", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Lesson title"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Lesson content"}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["content", "grade"]
        widgets = {
            "content": forms.TextInput(attrs={"class": "form-control", "placeholder": "Question text"}),
            "grade": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }
