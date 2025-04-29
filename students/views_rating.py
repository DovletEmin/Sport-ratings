from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ExerciseResult, Student
from django.db.models import Max

class RatingView(APIView):
    """
    View to get the rating of students based on their exercise results.
    """
    def get(self, request):
        exercise_types = {
            'pull_over': 'Turnikdan göwräňi aşyrmak',
            'pull_up': 'Turnik çekmek',
            'run': 'Ylgaw'
        }
        data = {}

        for exercise_code, exercise_name in exercise_types.items():
            best_results = (
                ExerciseResult.objects
                .filter(exercise_type=exercise_code)
                .values('student')  
                .annotate(best_value=Max('value'))
                .order_by('-best_value')
            )

            ranking = []
            for idx, result in enumerate(best_results, start=1):
                student = Student.objects.get(id=result['student'])
                ranking.append({
                    'rank': idx,
                    'student_id': student.student_id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'faculty': student.faculty,
                    'best_value': result['best_value']
                })

            data[exercise_code] = {
                'exercise_name': exercise_name,
                'ranking': ranking
            }

        return Response(data)

