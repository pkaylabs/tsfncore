from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Report, Notification
from apis.serializers import NotificationSerializer
from datetime import datetime, timedelta


class PingAPI(APIView):
    '''This view is used to check if the server is up and running'''
    def get(self, request):
        '''This method is used to check if the server is up and running'''
        return Response({'message': 'pong'}, status=status.HTTP_200_OK)


class DashboardAPIView(APIView):
    '''This view is used to get the dashboard data'''
    
    def get(self, request):
        '''This method is used to get the dashboard data'''
        user = request.user
        reports = Report.objects.filter(reported_by=user)
        notifications = Notification.objects.filter(reporter=user)
        
        # Get today's date
        today = datetime.today().date()
        
        # Determine the next reporting day (Monday - Friday)
        if today.weekday() == 4:  # Friday
            next_reporting_day = today + timedelta(days=3)  # Monday
        elif today.weekday() in [5, 6]:  # Saturday or Sunday
            next_reporting_day = today + timedelta(days=(7 - today.weekday()))  # Monday
        else:
            next_reporting_day = today + timedelta(days=1)  # Next weekday
        
        return Response({
            'reports': reports.count(),  # Total reports submitted by the user
            'total_reports': 54,  # Total reports in a year
            'next_reporting_day': next_reporting_day.strftime('%Y-%m-%d'),  # Next reporting date
            'notifications': NotificationSerializer(notifications, many=True).data
        }, status=status.HTTP_200_OK)

# class DashboardAPIView(APIView):
#     '''This view is used to get the dashboard data'''
#     def get(self, request):
#         '''This method is used to get the dashboard data'''
#         user = request.user
#         reports = Report.objects.filter(reported_by=user)
#         notifications = Notification.objects.filter(reporter=user)
#         # look for the next reporting day's date (Mon - Fri)
#         # if today is Friday, then the next reporting day is Monday
#         # if today is Monday, then the next reporting day is Tuesday
#         # if today is Tuesday, then the next reporting day is Wednesday
#         # if today is Wednesday, then the next reporting day is Thursday
#         # if today is Thursday, then the next reporting day is Friday
#         # if today is Saturday, then the next reporting day is Monday
#         # if today is Sunday, then the next reporting day is Monday
        
#         return Response({
#             'reports': reports.count(), # total reports submitted by the user
#             'total_reports': 54, # total reports in a year
#             'notifications': NotificationSerializer(notifications, many=True).data
#         }, status=status.HTTP_200_OK)