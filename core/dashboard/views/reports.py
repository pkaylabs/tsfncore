import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from apis.models import Report
from django.db.models import Q
from core.utils.contants import ReportStatus
from core.utils.decorators import StaffLoginRequired
from django.utils.decorators import method_decorator

from django.contrib import messages


class ReportView(View):
    template = 'dashboard/pages/reports.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        print(f"query: {query}")
        filtered = request.GET.get('form_id') == 'filter'
        reports = Report.objects.all().order_by('created_at')
        if query:
            reports = Report.objects.filter(
                Q(report_id__icontains=query)|
                Q(school__name__icontains=query)|
                Q(meal_type__icontains=query)|
                Q(comments__icontains=query)|
                Q(reported_by__name__icontains=query)|
                Q(status__icontains=query)
            ).order_by('created_at')

        if filtered:
            print('Filtered!!')
            report_status = request.GET.get('status')
            report_date = request.GET.get('report_date')
            created_at = request.GET.get('created_date')

            if report_status == '' or str(report_status).upper() == 'ALL':
                pass
            else:
                reports = reports.filter(status=report_status)
            if report_date:
                reports = reports.filter(date_of_report=report_date)
            if created_at:
                reports = reports.filter(created_at=created_at)

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
    


class DownloadReportsView(View):
    '''Download reports as csv'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        reports = Report.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reports.csv"'
        writer = csv.writer(response)
        writer.writerow(['Report ID', 'School', 'Students Enrolled', 'Students Fed', 'Meal Type', 'Comments', 'Status', 'Reported By', 'Created At']) # noqa
        for report in reports:
            writer.writerow([report.report_id, report.school.name, report.students_enrolled, report.students_fed, report.meal_type, report.comments, report.status, report.reported_by.name, report.created_at])
        return response