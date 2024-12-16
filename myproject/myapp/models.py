from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import UserManager


# Intermediate model for User - Group Many-to-Many relationship
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission

# Optimized User-Group relationship
class UserGroup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} - {self.group}"

# Optimized User-Permission relationship (Many-to-Many)
class UserPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'permission')

    def __str__(self):
        return f"{self.user.username} - {self.permission.name}"


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('staff', 'Staff'),
    ]


    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=50, default='user')
    department = models.CharField(max_length=50, default='')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class GrievanceCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


    def __str__(self):
        return self.name
   
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    head = models.CharField(max_length=100, unique=True,default='admin')
    description = models.TextField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    
class Priority(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    




class Grievance(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]


    user = models.CharField(max_length=200,default='anonyms') #models.ForeignKey(User, on_delete=models.CASCADE, related_name="grievances")
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=200,default='security') #models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    department = models.CharField(max_length=200,default='Technical') #models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="grievances")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title




class GrievanceAttachment(models.Model):
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to='grievance_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Attachment for {self.grievance.title}"


class Feedback(models.Model):
    grievance = models.OneToOneField(Grievance, on_delete=models.CASCADE, related_name="feedback")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Feedback for {self.grievance.title}"


class Report(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    grievance_count = models.IntegerField()
    resolved_count = models.IntegerField()
    escalated_count = models.IntegerField()
    average_resolution_time = models.DurationField()


    def __str__(self):
        return f"Report from {self.start_date} to {self.end_date}"






#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
