from django.contrib import admin
from .models import Student, ExerciseResult

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id')
    search_fields = ('first_name', 'last_name', 'student_id')


class ExerciseResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'result', 'date')
    list_filter = ('date')
    search_fields = ('student__first_name', 'student__last_name')


admin.site.register(Student)
admin.site.register(ExerciseResult)