from django.shortcuts import render
def home(request):
    return render(request,'home.html')
from django.conf import settings
# Create your views here.
# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, QuestionAnswer
from .forms import ProjectForm, QuestionAnswerForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.shortcuts import redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm
def features(request):
    return render(request,"features.html")
def services(request):
    return render(request,"services.html")
@login_required
def create_project_view(request):
    # Check if user already has a project
    existing_project = Project.objects.filter(user=request.user).first()

    # If project exists, redirect to the edit page
    if existing_project:
        return redirect('edit_project', pk=existing_project.pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Ensure project belongs to logged-in user
            project.save()
            return redirect('edit_project', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {
        'form': form
    })


@login_required
def edit_project_view(request, pk):
    # Safely fetch the project for the current user
    try:
        project = Project.objects.get(pk=pk, user=request.user)
    except Project.DoesNotExist:
        return redirect('create_project')  # Graceful fallback

    # Setup the formset for QuestionAnswer linked to this project
    QAFormSet = modelformset_factory(
        QuestionAnswer,
        form=QuestionAnswerForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        formset = QAFormSet(request.POST, request.FILES, queryset=project.qas.all())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.project = project
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('edit_project', pk=pk)
    else:
        formset = QAFormSet(queryset=project.qas.all())

    return render(request, 'edit_project.html', {
        'project': project,
        'formset': formset,
    })

@login_required
def dashboard(request):
    return render(request,"dashboard.html")
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import *
from .models import OTPVerification

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from .forms import SignupForm, OTPForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import OTPVerification

# 🔹 Signup
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            otp_obj, _ = OTPVerification.objects.get_or_create(user=user)
            otp_obj.generate_otp()

            send_mail(
                "Your OTP Code",
                f"Your OTP is: {otp_obj.otp}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            request.session['uid'] = user.id
            return redirect('verify_otp')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# 🔹 Verify OTP
def verify_otp_view(request):
    uid = request.session.get('uid')
    user = get_object_or_404(User, id=uid)
    otp_obj = get_object_or_404(OTPVerification, user=user)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == otp_obj.otp:
                user.is_active = True
                user.save()
                otp_obj.delete()
                messages.success(request, "Account verified! Please log in.")
                return redirect('login')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})


# 🔹 Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')  # or dashboard
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# 🔹 Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# 🔹 Forgot Password
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp_obj, _ = OTPVerification.objects.get_or_create(user=user)
                otp_obj.generate_otp()

                send_mail(
                    "Reset OTP Code",
                    f"Your OTP is: {otp_obj.otp}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

                request.session['uid'] = user.id
                return redirect('reset_otp')
            except User.DoesNotExist:
                form.add_error('email', 'Email not found')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})


# 🔹 Reset OTP
def reset_otp_view(request):
    uid = request.session.get('uid')
    user = get_object_or_404(User, id=uid)
    otp_obj = get_object_or_404(OTPVerification, user=user)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == otp_obj.otp:
                return redirect('reset_password')
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'reset_otp.html', {'form': form})


# 🔹 Reset Password
def reset_password_view(request):
    uid = request.session.get('uid')
    user = get_object_or_404(User, id=uid)

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            OTPVerification.objects.filter(user=user).delete()
            messages.success(request, "Password reset successful.")
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})
@login_required
def my_projects_view(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'my_projects.html', {'projects': projects})
def build_context_prompt(project, user_question):
    qas = project.qas.all()
    context = "\n".join(
        f"Q{idx+1}: {qa.question}\nA{idx+1}: {qa.answer}"
        for idx, qa in enumerate(qas)
    )

    return f"""
You are a strict assistant. Only answer based on the context provided below.
Do NOT make up any answers or add extra information.

Context:
{context}

If the answer is not found in the above context, respond exactly:
"I'm sorry, I couldn't find an answer based on the provided project questions."

Now answer this question strictly using the context:

User Question: {user_question}
Answer:"""

import requests
from .models import Project


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt


from django.conf import settings
def generate_openrouter_answer(project_id, user_question):
    project = Project.objects.get(pk=project_id)
    prompt = build_context_prompt(project, user_question)

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_KEY}",

        "Referer": "https://www.aisearchlibrary.in",
        "X-Title": "Project Chatbot",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # or claude/gpt
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    print("DEBUG status:", response.status_code)
    print("DEBUG response:", response.text)  # <-- Add this

    try:
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("DEBUG parse error:", str(e))
        return "Sorry, I couldn't fetch a response from the AI."

@csrf_exempt
def ask_bot(request, project_id):
    if request.method == 'POST':
        try:
            question = request.POST.get('question')
            answer = generate_openrouter_answer(project_id, question)
            return JsonResponse({'answer': answer})
        except Exception as e:
            import traceback
            print("ERROR in ask_bot:", str(e))
            traceback.print_exc()
            return JsonResponse({'error': 'Internal server error'}, status=500)



@login_required
def chatbot_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    return render(request, 'chatbot.html', {'project': project})
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from home.models import Project

def embed_chatbot(request):
    bot_key = request.GET.get('key')
    if not bot_key:
        raise Http404("Missing 'key' parameter in URL")

    project = get_object_or_404(Project, bot_key=bot_key)
    return render(request, 'embed_chatbot.html', {'project': project})

@login_required
def project_summary_view(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    return render(request, 'project_summary.html', {'project': project})
from django.shortcuts import render
from django.http import HttpResponse

def robots_txt(request):
    return render(request, 'robots.txt', content_type='text/plain')

def sitemap_xml(request):
    return render(request, 'sitemap.xml', content_type='application/xml')
