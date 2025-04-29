from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# Настроим схему документации
schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Тут описание вашего API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

# Создайте маршруты для API
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]