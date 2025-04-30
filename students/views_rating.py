from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import ExerciseResult, Student
from django.db.models import Max, Sum, Q
from collections import defaultdict

class BaseExerciseRatingView(APIView):
    exercise_type = None
    exercise_name = None

    def get(self, request):
        faculty = request.query_params.get('faculty')
        group = request.query_params.get('group')

        students = Student.objects.all()
        if faculty:
            students = students.filter(faculty=faculty)
        if group:
            students = students.filter(group=group)

        student_ids = students.values_list('id', flat=True)

        best_results = (
            ExerciseResult.objects
            .filter(exercise_type=self.exercise_type, student_id__in=student_ids)
            .values('student')
            .annotate(best_value=Max('value'))
            .order_by('best_value' if self.exercise_type == 'run' else '-best_value')
        )

        paginator = PageNumberPagination()
        paginated_results = paginator.paginate_queryset(best_results, request)

        start_rank = (paginator.page.number - 1) * paginator.page.paginator.per_page + 1
        ranking = []
        for idx, result in enumerate(paginated_results, start=start_rank):
            student = Student.objects.get(id=result['student'])
            ranking.append({
                'rank': idx,
                'student_id': student.student_id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'faculty': student.faculty,
                'group': student.group,
                'best_value': result['best_value']
            })

        return paginator.get_paginated_response({
            'exercise_type': self.exercise_type,
            'exercise_name': self.exercise_name,
            'ranking': ranking
        })
    

class OverallRatingView(APIView):
    def get(self, request):
        faculty = request.query_params.get('faculty')
        group = request.query_params.get('group')

        students = Student.objects.all()
        if faculty:
            students = students.filter(faculty=faculty)
        if group:
            students = students.filter(group=group)

        student_ids = students.values_list('id', flat=True)

        exercise_types = ['pull_up', 'pull_over', 'run']
        best_scores = defaultdict(float)

        for exercise in exercise_types:
            best_results = (
                ExerciseResult.objects
                .filter(student_id__in=student_ids, exercise_type=exercise)
                .values('student')
                .annotate(best_value=Max('value'))
            )

            for res in best_results:
                best_scores[res['student']] += res['best_value']

        sorted_scores = sorted(best_scores.items(), key=lambda x: x[1], reverse=True)

        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(sorted_scores, request)

        ranking = []
        start_rank = (paginator.page.number - 1) * paginator.page.paginator.per_page + 1

        for idx, (student_id, total_score) in enumerate(paginated, start=start_rank):
            student = Student.objects.get(id=student_id)
            ranking.append({
                'rank': idx,
                'student_id': student.student_id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'faculty': student.faculty,
                'group': student.group,
                'total_score': round(total_score, 2)
            })

        return paginator.get_paginated_response({"ranking": ranking})


class PullOverRatingView(BaseExerciseRatingView):
    exercise_type = 'pull_over'
    exercise_name = 'Turnikdan göwräni aşyrmak'

class PullUpRatingView(BaseExerciseRatingView):
    exercise_type = 'pull_up'
    exercise_name = 'Turnik çekmek'

class RunRatingView(BaseExerciseRatingView):
    exercise_type = 'run'
    exercise_name = 'Ylgaw'