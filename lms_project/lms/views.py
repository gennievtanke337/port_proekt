from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Lesson, Module, Assignment, Submission, Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User




def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrolled = False
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    modules = course.modules.all()

    return render(request, 'lms/course_detail.html', {
        'course': course,
        'modules': modules,
        'enrolled': enrolled
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'lms/register.html', {'form': form})

def home(request):
    courses = Course.objects.all()
    return render(request, 'lms/home.html', {'courses': courses})

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not hasattr(request.user, 'profile'):
                Profile.objects.create(user=request.user, role='student')
            if request.user.profile.role in ['teacher', 'admin'] or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Доступ заборонено: потрібен викладач")
    return _wrapped_view


@login_required
@teacher_required
def create_lesson(request, module_id):
    module = get_object_or_404(Module, id=module_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        video_url = request.POST.get('video_url')
        Lesson.objects.create(module=module, title=title, content=content, video_url=video_url)
        return redirect('module_detail', module_id=module.id)

    return render(request, 'lms/create_lesson.html', {'module': module})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    return redirect('course_detail', course_id=course.id)

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course
    enrolled = request.user.is_authenticated and Enrollment.objects.filter(user=request.user, course=course).exists()
    user_submissions = {}
    if request.user.is_authenticated:
        for assignment in lesson.assignments.all():
            user_submissions[assignment.id] = Submission.objects.filter(
                assignment=assignment,
                student=request.user
            ).exists()
    return render(request, 'lms/lesson_detail.html', {
        'lesson': lesson,
        'enrolled': enrolled,
        'user_submissions': user_submissions
    })

def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    enrolled = False
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=module.course
        ).exists()
    if not enrolled:
        return redirect('course_detail', module.course.id)
    return render(request, 'lms/module_detail.html', {'module': module})

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission, created = Submission.objects.get_or_create(
        assignment=assignment,
        student=request.user
    )
    if request.method == 'POST':
        submission.answer = request.POST.get('answer')
        submission.save()
        return redirect('lesson_detail', lesson_id=assignment.lesson.id)
    return render(request, 'lms/submit_assignment.html', {
        'assignment': assignment,
        'submission': submission
    })

@login_required
def manage_roles(request):
    if not request.user.is_superuser and request.user.profile.role != 'admin':
        return HttpResponseForbidden("Доступ заборонено")
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        for user_id, role in request.POST.items():
            if user_id.startswith("role_"):
                uid = int(user_id.split("_")[1])
                user_obj = User.objects.get(id=uid)
                if role == 'admin' and not request.user.is_superuser:
                    continue
                profile = user_obj.profile
                profile.role = role
                profile.save()
        return redirect('manage_roles')
    return render(request, 'lms/manage_roles.html', {'users': users})

@login_required
@teacher_required
def select_module(request):
    modules = Module.objects.all()
    return render(request, 'lms/select_module.html', {'modules': modules})


@login_required
@teacher_required
def select_module(request):
    modules = Module.objects.all() 
    return render(request, 'lms/select_module.html', {'modules': modules})