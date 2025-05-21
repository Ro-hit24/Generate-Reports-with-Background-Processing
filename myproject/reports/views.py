from django.shortcuts import render

# Create your views here.

from django.views import View
from django.http import JsonResponse
from .models import Report
from .tasks import generate_and_send_report

class RequestReportView(View):
    def post(self, request, *args, **kwargs):
        # Create a new report entry
        report = Report.objects.create(user=request.user)
        
        # Trigger the background task to generate and send the report
        generate_and_send_report.delay(report.id)
        
        # Return a response indicating the report generation has started
        return JsonResponse({'status': 'Report generation started', 'report_id': report.id})
