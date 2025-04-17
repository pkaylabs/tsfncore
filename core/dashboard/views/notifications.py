import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from apis.models import Notification
from core.utils.decorators import StaffLoginRequired
from django.utils.decorators import method_decorator
from django.db.models import Q

class NotificationsView(View):
    '''notifications view'''
    template = 'dashboard/pages/notifications.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        '''gets all notifications'''
        query = request.GET.get('query')
        notifications = Notification.objects.all().order_by('-created_at')
        if query:
            notifications = Notification.objects.filter(
                Q(reporter__name__icontains=query)|
                Q(message__icontains=query)
            )
        context = {
            "notifications": notifications
        }
        return render(request, self.template, context)
    
class DownloadNotificationsView(View):
    '''Download notifications as csv'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        notifications = Notification.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="notifications.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Reporter', 'Message', 'Created At']) # noqa
        for notification in notifications:
            writer.writerow([notification.id, notification.reporter.name, notification.message, notification.created_at])
        return response