from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.utils.timezone import now
from login.models import LoginStudent
from t_dashboard.models import Test, Question
from .models import TestResult, StudentAnswer
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from django.db.models import F


def student_dashboard(request):
    student_username = request.session.get("s_username")
    if not student_username:
        return HttpResponse("No student profile found")

    try:
        student = LoginStudent.objects.get(username=student_username)
    except LoginStudent.DoesNotExist:
        return HttpResponse("Student not found")

    # Get all relevant tests for the student
    tests = Test.objects.filter(
        department=student.dept, year_of_study=student.year
    ).order_by("date_of_test", "start_time")

    # Process each test
    processed_tests = []
    has_active_tests = False
    for test in tests:
        status, time_info = test.get_status()
        if status == "in_progress":
            has_active_tests = True

        test_info = {
            "test": test,
            "status": status,
            "can_start": test.can_start_test(),
        }

        # Check if student has already completed this test
        try:
            result = TestResult.objects.get(student=student, test=test)
            test_info["completed"] = True
            test_info["score"] = result.score
        except TestResult.DoesNotExist:
            test_info["completed"] = False

        # Add time information based on status
        if status == "upcoming":
            hours = time_info.total_seconds() // 3600
            minutes = (time_info.total_seconds() % 3600) // 60
            test_info["time_to_start"] = f"{int(hours)}h {int(minutes)}m"
        elif status == "in_progress":
            minutes = time_info.total_seconds() // 60
            test_info["time_remaining"] = f"{int(minutes)} minutes"

        processed_tests.append(test_info)

    return render(
        request,
        "student_dashboard.html",
        {
            "tests": processed_tests,
            "student": student,
            "has_active_tests": has_active_tests,
        },
    )


def start_test(request):
    student_username = request.session.get("s_username")
    if not student_username:
        return HttpResponse("No student profile found")

    test_id = request.GET.get("test_id")
    if not test_id:
        return HttpResponse("No test specified")

    test = get_object_or_404(Test, test_id=test_id)
    student = get_object_or_404(LoginStudent, username=student_username)

    # Check if student has already completed this test
    if TestResult.objects.filter(student=student, test=test).exists():
        return HttpResponse("You have already completed this test")

    # Verify the test can be started
    if not test.can_start_test():
        return HttpResponse("This test cannot be started at this time")

    # Get all questions for this test
    questions = Question.objects.filter(test=test)
    total_questions = questions.count()

    # If this is the initial request, show instructions
    if not request.GET.get("started"):
        return render(
            request,
            "test_instructions.html",
            {
                "test": test,
                "total_questions": total_questions,
            },
        )

    # Calculate time remaining
    ist = pytz.timezone("Asia/Kolkata")
    now = timezone.now().astimezone(ist)
    test_datetime = datetime.combine(test.date_of_test, test.start_time)
    test_datetime = ist.localize(test_datetime)

    h, m, s = map(int, test.duration.split(":"))
    duration = timedelta(hours=h, minutes=m, seconds=s)
    end_time = test_datetime + duration
    time_remaining = end_time - now

    # Convert time remaining to minutes:seconds format
    minutes = int(time_remaining.total_seconds() // 60)
    seconds = int(time_remaining.total_seconds() % 60)
    time_remaining_str = f"{minutes}:{seconds:02d}"

    return render(
        request,
        "test_questions_new.html",
        {
            "test": test,
            "questions": questions,
            "time_remaining": time_remaining_str,
        },
    )


def submit_test(request, test_id):
    if request.method != "POST":
        return HttpResponse("Invalid request method")

    student_username = request.session.get("s_username")
    if not student_username:
        return HttpResponse("No student profile found")

    test = get_object_or_404(Test, test_id=test_id)
    student = get_object_or_404(LoginStudent, username=student_username)
    questions = Question.objects.filter(test=test)

    # Check if student has already completed this test
    if TestResult.objects.filter(student=student, test=test).exists():
        return HttpResponse("You have already completed this test")

    # Create test result
    correct_answers = 0
    total_questions = questions.count()

    test_result = TestResult.objects.create(
        student=student, test=test, total_questions=total_questions
    )

    # Process each answer
    for question in questions:
        selected_option = request.POST.get(f"q{question.question_id}")
        if selected_option:
            is_correct = selected_option == question.correct_option
            if is_correct:
                correct_answers += 1

            StudentAnswer.objects.create(
                test_result=test_result,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct,
            )

    # Calculate and save score
    score = int((correct_answers / total_questions) * 100)
    test_result.score = score
    test_result.correct_answers = correct_answers
    test_result.save()

    return redirect("test_result", test_id=test_id)


def test_result(request, test_id):
    student_username = request.session.get("s_username")
    if not student_username:
        return HttpResponse("No student profile found")

    test = get_object_or_404(Test, test_id=test_id)
    student = get_object_or_404(LoginStudent, username=student_username)
    result = get_object_or_404(TestResult, student=student, test=test)

    # Get leaderboard
    leaderboard = TestResult.objects.filter(test=test).order_by("-score")[:10]

    return render(
        request,
        "test_result.html",
        {"test": test, "result": result, "leaderboard": leaderboard},
    )


# Create your views here.
