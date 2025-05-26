from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView

from apis.models import School
from apis.serializers import SchoolSerializer


class SchoolsAPIView(APIView):
    '''This view is used to get all schools'''
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        '''
            This method is used to get all schools.
            for the currently logged in user.
        '''
        schools = School.objects.all().order_by('name')
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)