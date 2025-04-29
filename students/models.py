from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    student_id = models.IntegerField(max_length=10, unique=True)
    faculty = models.CharField(max_length=100)
    group = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()
    photo = models.ImageField(upload_to='student/photos/', null=True, blank=True)

    def __str__(self):
        return f"({self.student_id}) {self.first_name} {self.last_name}"
    
    def bmi(self):
        if self.height > 0:
            return round(self.weight / (self.height * self.height), 1)
        return None
    

class ExerciseResult(models.Model):
    EXERCISE_CHOISES = [
        ('pull_over', 'Turnikdan göwräňi aşyrmak'),
        ('pull_up', 'Turnik çekmek'),
        ('run', 'Ylgaw'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exercise_results')
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_CHOISES)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
          return f"{self.student} - {self.get_exercise_type_display()} - {self.value} ({self.date.strftime('%Y-%m')})"