"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login_form'),
    path('register/',views.register_view, name ='registration_form'),
    path('forget/',views.forget_view, name ='forget_form'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('', views.homepage, name='homepage'),
    path('logout/',views.logout,name='logout'),
    path('grievance/',views.grievance,name='grievance'),
    path('complaints/',views.complaints,name='complaints'),
    path('', include('django.contrib.auth.urls')),
    path('feedback/', views.feedback, name='feedback'),
    path('department/<str:department_name>/', views.department_dashboard, name='department_dashboard'),
]