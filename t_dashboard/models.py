from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
import pytz


class Test(models.Model):
    test_id = models.AutoField(primary_key=True)  # Unique Test ID
    subject = models.CharField(max_length=255)  # Subject Name
    subject_code = models.CharField(max_length=50)  # Subject Code
    date_of_test = models.DateField()  # Test Date
    start_time = models.TimeField()  # Test Start Time
    duration = models.CharField(max_length=8)  # Test Duration (HH:MM:SS format)
    department = models.CharField(max_length=100)  # Department Name
    year_of_study = models.IntegerField()  # Year of Study (1, 2, 3, etc.)

    def __str__(self):
        return f"{self.subject} - {self.subject_code}"

    def can_start_test(self):
        """Check if the test can be started based on current time in IST"""
        ist = pytz.timezone("Asia/Kolkata")
        now = timezone.now().astimezone(ist)
        test_datetime = datetime.combine(self.date_of_test, self.start_time)
        test_datetime = ist.localize(test_datetime)

        # Parse duration (HH:MM:SS)
        h, m, s = map(int, self.duration.split(":"))
        duration = timedelta(hours=h, minutes=m, seconds=s)
        end_time = test_datetime + duration

        # Test can be started if current time is between start time and end time
        return test_datetime <= now <= end_time

    def get_status(self):
        """Get the current status of the test in IST"""
        ist = pytz.timezone("Asia/Kolkata")
        now = timezone.now().astimezone(ist)
        test_datetime = datetime.combine(self.date_of_test, self.start_time)
        test_datetime = ist.localize(test_datetime)

        h, m, s = map(int, self.duration.split(":"))
        duration = timedelta(hours=h, minutes=m, seconds=s)
        end_time = test_datetime + duration

        if now < test_datetime:
            time_to_start = test_datetime - now
            return "upcoming", time_to_start
        elif now > end_time:
            return "completed", None
        else:
            time_remaining = end_time - now
            return "in_progress", time_remaining


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)  # Remove default value
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=50
    )  # Stores "option1", "option2", etc.
    points = models.IntegerField(default=1)

    def __str__(self):
        return f"Question {self.question_id} - {self.test.subject}"


# Create your models here.
