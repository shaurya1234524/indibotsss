# projects/forms.py
from django import forms
from .models import Project, QuestionAnswer

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ['question', 'answer', 'image', 'image_description']
        widgets = {
            'answer': forms.Textarea(attrs={'rows': 3}),
            'image_description': forms.TextInput(attrs={'placeholder': 'Optional image caption'}),
        }


from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
