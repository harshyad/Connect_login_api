from rest_framework import serializers
from .models import student_models,teacher_models

class Imageserializer(serializers.ModelSerializer):
    class Meta:
        model=student_models
        fields = "__all__"

class teacherserializer(serializers.ModelSerializer):
    class Meta:
        model=teacher_models
        fields = "__all__"