from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required

def home(request):
    courses = Course.objects.all()
    return render(request, 'lms/home.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrolled = False

    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    return render(request, 'lms/course_detail.html', {
        'course': course,
        'enrolled': enrolled
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    return redirect('course_detail', course_id=course.id)
