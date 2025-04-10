from django.db.models import Sum
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone

from accounts.models import User
from apis.models import Report, School
from core.utils.contants import ReportStatus
from core.utils.decorators import StaffLoginRequired


class DashboardView(View):
    template = 'dashboard/pages/dashboard.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        # totals
        total_users = User.objects.count()
        total_schools = School.objects.count()
        total_reports = Report.objects.count()

        # aggregates
        reports_this_week = Report.objects.filter(created_at__week=timezone.now().isocalendar()[1]).count()
        reports_this_month = Report.objects.filter(created_at__month=timezone.now().month).count()
        
        verified_reports_this_week = Report.objects.filter(created_at__week=timezone.now().isocalendar()[1], status=ReportStatus.APPROVED.value).count()
        verified_reports_this_month = Report.objects.filter(created_at__month=timezone.now().month, status=ReportStatus.APPROVED.value).count()

        # counst for the months
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        # count the reports created in each month from jan-dec in a list
        reports_per_month = []
        verified_reports_per_month = []
        for month in range(1, 13):
            reports_per_month.append(Report.objects.filter(created_at__month=month).count())
            verified_reports_per_month.append(Report.objects.filter(created_at__month=month, status=ReportStatus.APPROVED.value).count())
        print("RPM", reports_per_month)
        print("VRPM", verified_reports_per_month)
        context ={
            'total_users': total_users,
            'total_schools': total_schools,
            'total_reports': total_reports,
            'reports_this_week': reports_this_week,
            'reports_this_month': reports_this_month,
            'verified_reports_this_week': verified_reports_this_week,
            'verified_reports_this_month': verified_reports_this_month,
            'reports_per_month': reports_per_month,
            'verified_reports_per_month': verified_reports_per_month,
            # 'reports_per_month': "|".join([str(i) for i in reports_per_month]),
            # 'verified_reports_per_month': "|".join([str(i) for i in verified_reports_per_month]),
            'months': months,
        }
        return render(request, self.template, context)