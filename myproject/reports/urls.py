# -*- coding: utf-8 -*-
from django.urls import path
from .views import RequestReportView

urlpatterns = [
    path('request_report/', RequestReportView.as_view(), name='request_report'),
]
