from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ExerciseResultViewSet
from .views_rating import RatingView

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'exercise-results', ExerciseResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rating/', RatingView.as_view(), name='rating'),
]