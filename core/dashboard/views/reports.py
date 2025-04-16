from django.shortcuts import render, redirect
from django.views import View
from apis.models import Report
from django.db.models import Q
from core.utils.contants import ReportStatus
from core.utils.decorators import StaffLoginRequired
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class ReportView(View):
    template = 'dashboard/pages/reports.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        reports = Report.objects.all().order_by('-created_at')
        context = {
            'reports': reports,
        }
        return render(request, self.template, context)

    def post(self, request):
        return redirect('reports')
    
class VerifyReportView(View):
    '''used to verify the reports submitted'''
    template = 'dashboard/pages/verify-report.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        report = Report.objects.filter(report_id=query).first()
        context = {
                'report': report
        }
        return render(request, self.template, context)
    
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        '''used to process the report: approve, reject, etc...'''

        report_id = request.POST.get('report_id')
        report_status = request.POST.get('status')
        report = Report.objects.filter(report_id=report_id).first()
        if not report:
            # somehow report wasn't found
            messages.success(request, "Couldn not find report")
            return redirect('dashboard:reports')
        approved_statuses = [ReportStatus.PENDING_REVIEW.value, ReportStatus.APPROVED.value, ReportStatus.REJECTED.value, ]
        if report_status in approved_statuses:
            report.status = report_status
            report.save()
            messages.success(request, "Report Processing Completed Succesfully")
        else:
            messages.error(request, "Selected status not allowed")
        return redirect('dashboard:reports')