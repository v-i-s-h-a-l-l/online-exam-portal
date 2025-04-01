from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import Test, Question
from s_dashboard.models import TestResult, StudentAnswer
from login.models import LoginStudent
from datetime import datetime
import pytz


def t_dashboard(request):
    username = request.session.get("t_username")
    staffid = request.session.get("t_staffid")
    emailid = request.session.get("t_emailid")
    dept = request.session.get("t_dept")
    return render(
        request,
        "teacher_dashboard.html",
        {"username": username, "staffid": staffid, "emailid": emailid, "dept": dept},
    )


def create_test(request):
    if request.method == "POST":
        subject_name = request.POST["subject_name"]
        subject_code = request.POST["subject_code"]
        date_of_test = request.POST["date_of_test"]
        start_time = request.POST["start_time"]
        duration = request.POST["duration"]
        department = request.POST["department"]
        year = request.POST["year"]

        # Create a new Test entry
        new_test = Test.objects.create(
            subject=subject_name,
            subject_code=subject_code,
            date_of_test=date_of_test,
            start_time=start_time,
            duration=duration,
            department=department,
            year_of_study=year,
        )
        print(new_test.test_id)
        request.session["testid"] = new_test.test_id

        return redirect("add_question")  # Redirect to test list page

    return render(request, "c_test.html")


def evaluate_test(request):
    # Get all tests
    tests = Test.objects.all()
    return render(request, "evaluate_test.html", {"tests": tests})


def test_details(request):
    tests = Test.objects.all()
    return render(request, "test_list.html", {"tests": tests})


def add_question(request):
    if request.GET.get("test_id"):
        testid = request.GET.get("test_id")
    else:
        testid = request.session.get("testid")
    num_questions = Question.objects.filter(test_id=testid).count() + 1
    if request.method == "POST":
        question_text = request.POST.get("question_text")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        correct_option = request.POST.get("correct_option")
        points = request.POST.get("points")

        # Save question to database
        Question.objects.create(
            test_id=testid,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            points=points,
        )
        # If "Finish" button is clicked, redirect to test details pag
        if "finish" in request.POST:
            return redirect("test_questions_list")
        # If "Next Question" is clicked, stay on the form
        return redirect("add_question")

    return render(
        request, "add_questions.html", {"test": testid, "question_no": num_questions}
    )


def test_questions_list(request):
    testid = request.GET.get("test_id")
    if not testid:
        return redirect("test_details")
    Questions = Question.objects.filter(test_id=testid)
    return render(
        request, "test_questions_list.html", {"Questions": Questions, "testid": testid}
    )


def delete_test(request, test_id):
    if request.method == "POST":
        test = get_object_or_404(Test, test_id=test_id)
        # Delete all questions associated with the test
        Question.objects.filter(test=test).delete()
        # Delete the test
        test.delete()
        messages.success(request, "Test deleted successfully!")
        return redirect("test_details")
    return redirect("test_details")


def student_answers(request, test_id, username):
    # Get the test and student
    test = get_object_or_404(Test, test_id=test_id)
    student = get_object_or_404(LoginStudent, username=username)

    # Get the test result
    result = get_object_or_404(TestResult, test=test, student=student)

    # Get all answers for this test and student
    student_answers = StudentAnswer.objects.filter(test_result=result)

    context = {
        "test": test,
        "student": student,
        "result": result,
        "student_answers": student_answers,
    }

    return render(request, "student_answers.html", context)


# Create your views here.
