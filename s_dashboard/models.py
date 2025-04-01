from django.db import models
from login.models import LoginStudent
from t_dashboard.models import Test, Question

# Create your models here.


class TestResult(models.Model):
    student = models.ForeignKey(LoginStudent, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)

    class Meta:
        unique_together = [
            "student",
            "test",
        ]  # Each student can have only one result per test


class StudentAnswer(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)  # option1, option2, etc.
    is_correct = models.BooleanField(default=False)
