from django.contrib import admin
from .models import Profile, Course, Module, Lesson, Assignment, Submission, Grade, Certificate

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')   
    list_editable = ('role',)         
    search_fields = ('user__username',)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and obj.role == 'admin':
            return  
        super().save_model(request, obj, form, change)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Grade)
admin.site.register(Certificate)
