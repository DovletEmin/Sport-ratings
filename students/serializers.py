from rest_framework import serializers
from .models import Student, ExerciseResult

class ExerciseResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseResult
        fields = ['id', 'exercise_type', 'value', 'date']


class StudentSerializer(serializers.ModelSerializer):
    exercise_results = ExerciseResultSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'student_id', 'faculty', 'group', 'height', 'weight', 'photo', 'bmi', 'exercise_results']

