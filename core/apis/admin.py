from django.contrib import admin

from .models import Notification, Report, ReportImage, School

admin.site.register(School)
admin.site.register(Report)
admin.site.register(ReportImage)
admin.site.register(Notification)
