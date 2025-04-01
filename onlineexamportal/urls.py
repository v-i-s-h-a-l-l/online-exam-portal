"""onlineexamportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from login.views import home, sucess, update_password, teacher_admin, logout
from t_dashboard.views import (
    create_test,
    evaluate_test,
    test_details,
    t_dashboard,
    add_question,
    test_questions_list,
    delete_test,
)
from s_dashboard.views import student_dashboard, start_test, submit_test, test_result

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", home, name="home"),
    path("sucess/", sucess, name="sucess"),
    path("update-password/", update_password, name="update_password"),
    path("teacher_admin/", teacher_admin, name="teacher_admin"),
    path("t_dashboard/", t_dashboard, name="t_dashboard"),
    path("create-test/", create_test, name="create_test"),
    path("evaluate-test/", evaluate_test, name="evaluate_test"),
    path("test-details/", test_details, name="test_details"),
    path("add_question/", add_question, name="add_question"),
    path("test_questions_list", test_questions_list, name="test_questions_list"),
    path("student_dashboard/", student_dashboard, name="student_dashboard"),
    path("logout/", logout, name="logout"),
    path("start_test/", start_test, name="start_test"),
    path("submit_test/<int:test_id>/", submit_test, name="submit_test"),
    path("test_result/<int:test_id>/", test_result, name="test_result"),
    path("delete_test/<int:test_id>/", delete_test, name="delete_test"),
]
