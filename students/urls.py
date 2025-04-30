from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ExerciseResultViewSet
from .views_rating import PullOverRatingView, PullUpRatingView, RunRatingView, OverallRatingView

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'exercise-results', ExerciseResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rating/pull_over/', PullOverRatingView.as_view(), name='rating_pull_over'),
    path('rating/pull_up/', PullUpRatingView.as_view(), name='rating_pull_up'),
    path('rating/run/', RunRatingView.as_view(), name='rating_run'),
    path('rating/overall/', OverallRatingView.as_view(), name='rating_overall'),
]