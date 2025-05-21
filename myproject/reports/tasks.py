# reports/tasks.py
from celery import shared_task, chain
from .models import Report
from django.core.mail import send_mail                                               
from django.conf import settings
from django.utils import timezone

@shared_task(bind=True)
def update_report_progress(self, report_id, progress):
    report = Report.objects.get(id=report_id)
    report.content = f"Generated {progress * 10}% of the report."
    report.save()
    self.update_state(state='PROGRESS', meta={'current': progress, 'total': 10})

@shared_task(bind=True)
def finalize_report(self, report_id):
    report = Report.objects.get(id=report_id)
    report.status = 'completed'
    report.content = f"Report completed for user: {report.user.username}"
    report.save()

    send_mail(
        'Your Requested Report',
        report.content,
        settings.DEFAULT_FROM_EMAIL,
        [report.user.email],
    )
    report.sent_at = timezone.now()
    report.save()

@shared_task(bind=True)
def generate_and_send_report(self, report_id):
    report = Report.objects.get(id=report_id)
    report.status = 'pending'
    report.save()

    # Create a chain of tasks to update progress and finalize the report
    progress_tasks = [update_report_progress.s(report_id, i) for i in range(1, 11)]
    task_chain = chain(*progress_tasks, finalize_report.s(report_id))
    task_chain()
