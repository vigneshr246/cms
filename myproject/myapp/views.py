from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from .models import User,Grievance,Category
from .forms import FeedbackForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Grievance
from django.contrib import admin
from django.db.models.functions import TruncDate
from django.db.models import Count

import json
from django.shortcuts import render
from .models import Grievance, Feedback
from django.db.models import Count

def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('home')

    status_counts = Grievance.objects.values('status').annotate(count=Count('status'))
    status_data = {status['status']: status['count'] for status in status_counts}
    total_complaints = Grievance.objects.count()
    all_complaints = Grievance.objects.all()
    feedbacks = Feedback.objects.all()
    total_fb = Feedback.objects.count()
    timeline_data = Grievance.objects.annotate(date=TruncDate('created_at')) \
                                    .values('date') \
                                    .annotate(count=Count('id')) \
                                    .order_by('date')

    formatted_timeline_data = [
        {'date': str(item['date']), 'count': item['count']} 
        for item in timeline_data
    ]
    context = {
        'status_data': json.dumps(status_data),
        'timeline_data': json.dumps(formatted_timeline_data),
        'total_complaints': total_complaints,
        'all_complaints': all_complaints,
        'feedbacks' : feedbacks,
        'countfb' : total_fb,
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
    name = request.user.name
    ticket = User.objects.filter(Q(name=name))
    context = {
        'ticket' : ticket,
    }
    print(context)
    return render(request, 'myapp/user_dashboard.html',context)

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

from django.db.models import Q


def grievance(request):
    
    name = request.user.name
    ticket = Grievance.objects.filter(Q(user=name))
    context = {
        'tickets' : ticket,
    }
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


    return render(request, 'myapp/grievance.html',context)






@login_required
def feedback(request):
    # Filter grievances for the logged-in user with status 'escalated' or 'resolved'
    user_name = request.user.name  # Assuming the User model has a 'name' field
    user_grievances = Grievance.objects.filter(
        Q(user=user_name) & Q(status__in=['escalated', 'resolved'])
    )

    # Handle GET and POST requests
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            grievance_title = form.cleaned_data.get('grievance')  # Use cleaned_data for safety
            try:
                grievance = Grievance.objects.get(title=grievance_title, user=user_name)
                # Check if feedback already exists for this grievance
                if not Feedback.objects.filter(grievance=grievance).exists():
                    feedback = form.save(commit=False)
                    feedback.user = request.user
                    feedback.grievance = grievance
                    feedback.save()
                    return redirect('user_dashboard')  # Redirect on successful feedback submission
                else:
                    error_message = "Feedback already exists for this grievance."
            except Grievance.DoesNotExist:
                error_message = "Selected grievance does not exist."
        else:
            error_message = "Invalid form submission."
    else:
        form = FeedbackForm()
        error_message = None

    # Render the feedback form
    return render(request, 'myapp/feedback.html', {
        'form': form,
        'user_grievances': user_grievances,
        'error_message': error_message
    })



def department_dashboard(request, department_name):
    if request.user.department != department_name:
        return HttpResponse("You are not authorized to view this page.", status=403)

    # Filter complaints and feedback for the particular department
    department_complaints = Grievance.objects.filter(department=department_name)
    department_feedback = Feedback.objects.filter(grievance__department=department_name)

    # Data for charts
    status_data = department_complaints.values('status').annotate(count=Count('id'))
    timeline_data = department_complaints.extra({'date': "DATE(created_at)"}).values('date').annotate(count=Count('id'))

    # Transform data for charts
    status_data_dict = {item['status']: item['count'] for item in status_data}
    timeline_data_list = [{'date': item['date'], 'count': item['count']} for item in timeline_data]

    # Count totals
    total_complaints = department_complaints.count()
    total_feedbacks = department_feedback.count()

    context = {
        'department_name': department_name,
        'total_complaints': total_complaints,
        'countfb': total_feedbacks,
        'all_complaints': department_complaints,
        'feedbacks': department_feedback,
        'status_data': status_data_dict,
        'timeline_data': timeline_data_list,
    }

    return render(request, 'department_dashboard.html', context)
