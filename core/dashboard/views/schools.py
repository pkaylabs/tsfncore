from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from apis.models import School
import csv
from django.contrib import messages
from django.db.models import Q
from core.utils.decorators import StaffLoginRequired
from django.utils.decorators import method_decorator
from dashboard.forms import SchoolForm


class SchoolsView(View):
    template = 'dashboard/pages/schools.html'
    def get(self, request):
        query = request.GET.get('query')
        schools = School.objects.all().order_by('-created_at')
        if query:
            schools = School.objects.filter(
                Q(name__icontains=query)|
                Q(phone__icontains=query)|
                Q(email__icontains=query)|
                Q(town__icontains=query) |
                Q(district__icontains=query) |
                Q(region__icontains=query)
            ).order_by('-created_at')
        context = {
            'schools': schools,
        }
        return render(request, self.template, context)

    def post(self, request):
        school_id = request.POST.get('school_id')
        school = School.objects.filter(id=school_id).first()
        form = SchoolForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            if school is not None:
                messages.success(request, 'School Updated Successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'School Created Successfully')
                return redirect('dashboard:schools')
        else:
            for k, v in form.errors():
                msg = f"{k}: {v}"
                messages.error(request, msg)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    def delete(self, request):
        '''delete school'''
        school_id = request.POST.get("school")
        school = School.objects.filter(id=school_id).first()
        if school is not None:
            school.delete()
            messages.success(request, "School Deleted Successfully")
            return redirect('dashboard:schools')
        else:
            messages.error(request, "School not found")
            return redirect('dashboard:schools')

    

class CreateUpdateSchoolView(View):
    template = 'dashboard/pages/create-update-school.html'
    def get(self, request):
        query =  request.GET.get('school')
        school = School.objects.filter(id=query).first()
        regions = [
        "Ahafo", "Ashanti", "Bono", "Bono East", "Central", "Eastern", "Greater Accra",
        "North East", "Northern", "Oti", "Savannah", "Upper East", "Upper West",
        "Volta", "Western", "Western North"
        ]
        context = {
            'school': school,
            'regions': regions
        }
        return render(request, self.template, context)

    def post(self, request):
        school_id = request.POST.get('school_id') or None
        school = School.objects.filter(id=school_id).first()
        form = SchoolForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            if school is not None:
                print(f"School: {school}")
                messages.success(request, 'School Updated Successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.success(request, 'School Created Successfully')
                return redirect('dashboard:schools')
        else:
            for k, v in form.errors.items():
                msg = f"{k}: {v}"
                messages.error(request, msg)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class DeleteSchoolView(View):
    '''view for deleting schools'''
    
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        school_id = request.POST.get("school_id")
        school = School.objects.filter(id=school_id).first()
        if school:
            school.delete()
            messages.success(request, "School deleted successfully.")
        else:
            messages.error(request, "School not found.")
        return redirect('dashboard:schools')

    
class DownloadSchoolsView(View):
    '''Download schools as csv'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        schools = School.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="schools.csv"'
        writer = csv.writer(response)
        writer.writerow(['primary_key', 'name', 'email', 'phone', 'region', 'district', 'town', 'created_at', 'logo']) # noqa
        for school in schools:
            base = "127.0.0.1:8000/"
            logo = f"{base}{school.logo.url}" if school.logo else "No Logo"
            writer.writerow([school.id, school.name, school.email, school.phone, school.region, school.district, school.town, school.created_at, logo])
        return response