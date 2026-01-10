from django.contrib import admin
from .models import (
    Profile,
    Course,
    Module,
    Lesson,
    Assignment,
    Submission,
    Grade,
    Certificate
)

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Grade)
admin.site.register(Certificate)
