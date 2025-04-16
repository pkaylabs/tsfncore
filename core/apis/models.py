from django.db import models

from accounts.models import User
from core.utils.contants import MealType, ReportStatus


class School(models.Model):
    '''School model'''
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    town = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    '''Report model'''
    def generate_report_id():
        '''generate a unique report id'''
        return 'RPT-' + str(int(Report.objects.count()) + 1).zfill(8)
    report_id = models.CharField(max_length=20, default=generate_report_id, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    students_enrolled = models.IntegerField(default=0)
    students_fed = models.IntegerField(default=0)
    meal_type = models.CharField(default=MealType.BREAKFAST.value, max_length=50)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default=ReportStatus.PENDING_REVIEW.value)

    # stamps
    reported_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    date_of_report = models.DateField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_report_images(self):
        '''get all report images attached to this report'''
        images = ReportImage.objects.filter(report=self)
        return [i.image.url for i in images]
    
    def get_color(self):
        '''get the color of the report based on the status'''
        if self.status == ReportStatus.PENDING_REVIEW.value:
            return 'secondary'
        elif self.status == ReportStatus.APPROVED.value:
            return 'primary'
        elif self.status == ReportStatus.REJECTED.value:
            return 'danger'
        else:
            return 'gray'



    def __str__(self):
        return self.school.name + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')
    

class ReportImage(models.Model):
    '''Model for storing the images attached to a report'''
    image = models.ImageField(upload_to='reports/', null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report
    

class Notification(models.Model):
    '''Model for storing targetted notifications to the reporters'''
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reporter.name + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')