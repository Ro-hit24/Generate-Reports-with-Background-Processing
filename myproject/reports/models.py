from django.db import models

# Create your models here.


from django.contrib.auth.models import User

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
