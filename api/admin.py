from django.contrib import admin
from .models import student_models,teacher_models

# Register your models here.
admin.site.register(student_models)
admin.site.register(teacher_models)
