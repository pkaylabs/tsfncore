from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from apis.models import Report
from apis.serializers import AddReportSerializer, GetReportSerializer


class SubmittedReportsAPIView(APIView):
    '''This view is used to get all submitted reports'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        '''
            This method is used to get all submitted reports
            for the currently logged in user
        '''
        user = request.user
        reports = Report.objects.filter(reported_by=user)
        serializer = GetReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
            This method is used to submit a new report
        '''
        data = request.data
        data['reported_by'] = request.user.id
        serializer = AddReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)