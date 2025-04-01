from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_dashboard, name="student_dashboard"),
    path("start_test/", views.start_test, name="start_test"),
    path("submit_test/<int:test_id>/", views.submit_test, name="submit_test"),
    path("test_result/<int:test_id>/", views.test_result, name="test_result"),
]
