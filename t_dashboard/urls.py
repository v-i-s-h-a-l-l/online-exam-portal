from django.urls import path
from . import views

urlpatterns = [
    path("", views.t_dashboard, name="t_dashboard"),
    path("create_test/", views.create_test, name="create_test"),
    path("add_question/", views.add_question, name="add_question"),
    path("test_questions_list/", views.test_questions_list, name="test_questions_list"),
    path("evaluate_test/", views.evaluate_test, name="evaluate_test"),
    path("test_details/", views.test_details, name="test_details"),
    path(
        "student_answers/<int:test_id>/<str:username>/",
        views.student_answers,
        name="student_answers",
    ),
]
