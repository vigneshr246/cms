from django.contrib import admin
from .models import Department,Category,Priority,User,Feedback
from django.shortcuts import render
from .models import Grievance
from django.db.models import Count
from django.db.models.functions import TruncDate
import json

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Priority)
admin.site.register(User)
admin.site.register(Feedback)
admin.site.register(Grievance)



