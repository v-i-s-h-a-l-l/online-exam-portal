import os
import django
from datetime import date, time

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlineexamportal.settings")
django.setup()

from t_dashboard.models import Test, Question
from django.contrib.auth.models import User


def create_sample_data():
    # Create a superuser
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("Created superuser: admin")

    # Create sample tests
    tests = [
        {
            "subject": "Python Programming",
            "subject_code": "PY101",
            "date_of_test": date(2024, 4, 15),
            "start_time": time(10, 0),
            "duration": "02:00:00",
            "department": "Computer Science",
            "year_of_study": 1,
            "questions": [
                {
                    "question_text": "What is Python?",
                    "option1": "A programming language",
                    "option2": "A snake",
                    "option3": "A text editor",
                    "option4": "An operating system",
                    "correct_option": "option1",
                    "points": 1,
                },
                {
                    "question_text": "Which of these is not a Python data type?",
                    "option1": "int",
                    "option2": "float",
                    "option3": "char",
                    "option4": "str",
                    "correct_option": "option3",
                    "points": 1,
                },
            ],
        },
        {
            "subject": "Database Management",
            "subject_code": "DB101",
            "date_of_test": date(2024, 4, 20),
            "start_time": time(14, 0),
            "duration": "03:00:00",
            "department": "Computer Science",
            "year_of_study": 2,
            "questions": [
                {
                    "question_text": "What is SQL?",
                    "option1": "A programming language",
                    "option2": "A database query language",
                    "option3": "A web framework",
                    "option4": "An operating system",
                    "correct_option": "option2",
                    "points": 1,
                },
                {
                    "question_text": "Which of these is not a SQL command?",
                    "option1": "SELECT",
                    "option2": "INSERT",
                    "option3": "PRINT",
                    "option4": "UPDATE",
                    "correct_option": "option3",
                    "points": 1,
                },
            ],
        },
    ]

    # Create tests and questions
    for test_data in tests:
        questions = test_data.pop("questions")
        test = Test.objects.create(**test_data)
        print(f"Created test: {test.subject}")

        for question_data in questions:
            question = Question.objects.create(test=test, **question_data)
            print(f"Created question: {question.question_text[:30]}...")


if __name__ == "__main__":
    create_sample_data()
    print("Sample data created successfully!")
