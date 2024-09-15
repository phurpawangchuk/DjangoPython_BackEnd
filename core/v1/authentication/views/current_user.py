from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ....utils.helpers.responses import CustomRenderer
from ...users.serializers import UserResponseSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    renderer_classes = [CustomRenderer]

    def get(self, request):
        serializer = UserResponseSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
