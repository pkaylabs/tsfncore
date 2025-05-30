from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from apis.models import Report
from apis.serializers import AddReportSerializer, GetReportSerializer


class SubmittedReportsAPIView(APIView):
    '''This view is used to get all submitted reports'''
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        '''
            This method is used to get all submitted reports
            for the currently logged in user
        '''
        user = request.user
        reports = Report.objects.filter(reported_by=user).order_by('-created_at')
        serializer = GetReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
            This method is used to submit a new report with images
        '''
        data = request.data.copy()
        data['reported_by'] = request.user.id
        
        # Handle list of images from Flutter
        files = request.FILES.getlist('images[]')
        if files:
            data['images'] = files

        serializer = AddReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)