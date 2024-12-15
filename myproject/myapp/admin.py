from django.contrib import admin
from .models import Department,Category,Priority,User
from django.shortcuts import render
from .models import Grievance
from django.db.models import Count
from django.db.models.functions import TruncDate
import json

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Priority)
admin.site.register(User)

class GrievanceAdmin(admin.ModelAdmin):
    change_list_template = "myapp/admin_dashboard.html"

    def changelist_view(self, request, extra_context=None):
        status_counts = Grievance.objects.values('status').annotate(count=Count('status'))
        status_data = {status['status']: status['count'] for status in status_counts}
        total_complaints = Grievance.objects.count()
        all_complaints = Grievance.objects.all()

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
            'all_complaints': all_complaints
        }
        return super().changelist_view(request, extra_context=context)

admin.site.register(Grievance, GrievanceAdmin)



