from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiRoot.as_view(), name='api_root'),
    path('api/performance_metrics/', views.PerformanceMetrics.as_view(), name='performance_metrics'),
]
