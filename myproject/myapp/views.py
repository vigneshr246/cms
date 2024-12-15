from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Grievance,Category
from .forms import GrievanceForm, LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Grievance
from django.db.models import Count
from datetime import datetime

import json
from django.shortcuts import render
from .models import Grievance
from django.db.models import Count

def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('home')

    # Data for Pie Chart (Status of Issues)
    grievance_status_count = Grievance.objects.values('status').annotate(count=Count('status')).order_by('status')

    # Data for Timeline (Total Issues Over Time)
    grievances_over_time = Grievance.objects.values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')

    # Prepare the data for the pie chart and timeline
    status_data = {status['status']: status['count'] for status in grievance_status_count}
    timeline_data = {
        str(grievance['created_at__date']): grievance['count'] for grievance in grievances_over_time
    }

    # Serialize the data to JSON
    status_data_json = json.dumps(status_data)
    timeline_data_json = json.dumps(timeline_data)

    context = {
        'status_data': status_data_json,
        'timeline_data': timeline_data_json,
    }

    return render(request, 'myapp/admin_dashboard.html', context)



def complaints(request):
    pass



@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        else:
            return redirect('user_dashboard')
    else:
        return render(request, 'myapp/home.html', {'form': LoginForm()})

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
    return render(request, 'myapp/home.html')

def user_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'user':
        return redirect('home')
    return render(request, 'myapp/user_dashboard.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        phone = request.POST.get('phone')
        checkbox = request.POST.get('checkbox', None)

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'myapp/home.html')  # Replace 'register' with your registration URL name
        if checkbox != 'yes':
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, 'myapp/home.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'myapp/home.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'myapp/home.html')

        user = User.objects.create_user(name=username, email=email,phone =phone, password=password,username=username)
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('user_dashboard')
    return render(request, 'home.html')

def forget_view(request):
    return render(request, 'myapp/home.html')

def homepage(request):
    return render(request, 'myapp/home.html')


@login_required
def logout(request):
    return render(request, 'myapp/home.html')


def grievance(request):
    
    if request.method == 'POST':
        user= request.POST.get('user')
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_name = request.POST.get('category')
        department_name = request.POST.get('department')
        if category_name:
            category = get_object_or_404(Category, name=category_name)
        if department_name:
            department = get_object_or_404(Category, name=department_name)
        priority = request.POST.get('priority')
        grievance = Grievance.objects.create(user= user,title =title,description =description,category = category,priority = priority,department=department)
        grievance.save()
        messages.success(request, "Ticket raised successfully")
        return redirect('user_dashboard')
    return render(request, 'myapp/grievance.html')

