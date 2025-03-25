from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from apis.models import Report
from apis.serializers import ReportSerializer


class SubmittedReportsAPIView(APIView):
    '''This view is used to get all submitted reports'''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReportSerializer

    def get(self, request):
        '''
            This method is used to get all submitted reports
            for the currently logged in user
        '''
        user = request.user
        reports = Report.objects.filter(reported_by=user)
        serializer = self.serializer_class(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)