'''
This module contains the models for the accounts.
It includes the User, and OTP models.
These models are used to store information about the users 
and their otp information.

'''

from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.utils.contants import ReportStatus
from core.utils.services import send_sms

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom User model for the application'''
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True, null=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=10, default="STAFF")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # notification flags
    allow_push_notification = models.BooleanField(default=True)
    allow_submission_alert= models.BooleanField(default=True)
    allow_general_updates = models.BooleanField(default=True)
    allow_weekly_reminders = models.BooleanField(default=True)

    # preferences
    prefered_email = models.EmailField(max_length=50, blank=True, null=True)
    prefered_phone = models.CharField(max_length=12, blank=True, null=True)

    deleted = models.BooleanField(default=False)  # Soft delete
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_from_app = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name']


    def reports_submitted(self) -> int:
        '''gets the total reports submitted by the user'''
        from apis.models import Report
        reports = Report.objects.filter(reported_by=self).count()
        return reports
    
    def rejected_reports(self) -> int:
        '''gets the total reports submitted by the user that are rejected'''
        from apis.models import Report
        reports = Report.objects.filter(reported_by=self, status=ReportStatus.REJECTED.value).count()
        return reports
    
    def approved_reports(self) -> int:
        '''gets the total reports submitted by the user that are approved'''
        from apis.models import Report
        reports = Report.objects.filter(reported_by=self, status=ReportStatus.APPROVED.value).count()
        return reports
    


    def __str__(self):
        return self.name

class OTP(models.Model):
    '''One Time Password model'''
    phone = models.CharField(max_length=100)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self) -> bool:
        '''Returns True if the OTP is expired'''
        return (self.created_at + timedelta(minutes=30)) < timezone.now()
    
    def send_otp(self) -> None:
        '''Send the OTP to the user'''
        msg = f'Welcome to the Transparent School Feeding Network.\nYour OTP is {self.otp}\n\nRegards,\nTSFN Team'
        send_sms(msg, [self.phone])
        print(msg)

    def __str__(self):
        return self.phone + ' - ' + str(self.otp)