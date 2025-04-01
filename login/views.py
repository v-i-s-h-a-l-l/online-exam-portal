from django.shortcuts import render

# views.py
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LoginStudent
from django.shortcuts import HttpResponse
from django.core.mail import send_mail
import random
from django.conf import settings
from .models import TeacherAdmin
from django.contrib.auth.hashers import make_password


def home(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = LoginStudent.objects.get(username=username)
            if user.password == "Amrita@123":
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.save()
                send_mail(
                    subject="Your Otp for Password Reset from Onlineexamportal",
                    message=f"your otp is {otp}. USe this otp to Verify",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.emailid],
                )
                request.session["reset_user"] = username
                messages.success(request, "Login successful!")
                return redirect("update_password")
            # Redirect to dashboard after login
            elif user.password == password:
                request.session["s_username"] = user.username
                request.session["s_dept"] = user.dept
                request.session["s_year"] = user.emailid
                request.session["s_emailid"] = user.year
                return redirect("student_dashboard")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect("home")
        except LoginStudent.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect("home")

    return render(request, "login.html")


def login(request):
    return HttpResponse("hi")


def sucess(request):
    return HttpResponse("hello, login suceesss")


def teacher_admin(request):
    if request.method == "POST":
        usertype = request.POST.get("usertype")
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = TeacherAdmin.objects.get(username=username)
            print(user)
            if user.password == "Amrita@123":
                """
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.save()
                send_mail(
                    subject="Your Otp for Password Reset from Onlineexamportal",
                    message=f"your otp is {otp}. USe this otp to Verify",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.emailid],
                )"""
                request.session["reset_user"] = username
                messages.success(request, "Login successful!")
                return redirect("update_password")
            # Redirect to dashboard after login
            elif user.password == password:
                request.session["t_username"] = user.username
                request.session["t_staffid"] = user.staffid
                request.session["t_emailid"] = user.emailid
                request.session["t_dept"] = user.dept
                return redirect("t_dashboard")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect("teacher_admin")
        except LoginStudent.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect("teacher_admin")
    return render(request, "teacher_admin.html")


def update_password(request):
    if "reset_user" not in request.session:
        messages.error(request, "Unauthorized access!")
        return redirect("teacher_admin")

    username = request.session["reset_user"]

    # ✅ Fetch user from either TeacherAdmin or LoginStudent
    user = TeacherAdmin.objects.filter(username=username).first() or LoginStudent.objects.filter(username=username).first()

    if not user:
        messages.error(request, "User not found!")
        return redirect("home")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # ✅ Validate OTP
        if not user.otp or entered_otp != user.otp:
            messages.error(request, "Invalid OTP! Please try again.")
            return redirect("update_password")

        # ✅ Check password match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match! Please try again.")
            return redirect("update_password")

        # ✅ Prevent setting a default password
        if new_password == "Amrita@123":
            messages.error(request, "New password cannot be 'Amrita@123'.")
            return redirect("update_password")

        # ✅ Hash the password before storing
        user.password = make_password(new_password)
        user.otp = ""  # ✅ Clear OTP after successful update
        user.save()

        # ✅ Clear session variable
        del request.session["reset_user"]

        messages.success(request, "Password updated successfully! Please login.")
        return redirect("student_dashboard")

    return render(request, "updatepassword.html")

def logout(request):
    # Clear all session data
    request.session.flush()
    # Redirect to home page
    return redirect("home")


# Create your views here.
