from django.shortcuts import render, get_object_or_404
from .models import Course
from django.contrib.auth.decorators import login_required

def home(request):
    courses = Course.objects.all()
    return render(request, 'lms/home.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'lms/course_detail.html', {'course': course})
