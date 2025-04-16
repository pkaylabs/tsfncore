from django.shortcuts import render, redirect
from django.views import View
from apis.models import Report

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class ReportView(View):
    template = 'dashboard/pages/reports.html'
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

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        report = Report.objects.filter(report_id=query).first()
        context = {
                'report': report
        }
        return render(request, self.template, context)
    
    def post(self, request):
        '''used to process the report: approve, reject, etc...'''

        messages.success(request, "Report Processing Simulation Completed Succesfully")
        return redirect('dashboard:reports')