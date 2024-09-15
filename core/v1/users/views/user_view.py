from injector import Injector
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ....utils.helpers.responses import CustomRenderer, formatPaginatedData
from ....utils.modules.app_module import AppModule
from ..services import UserService

injector = Injector([AppModule()])


class UserView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [CustomRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = injector.get(UserService)

    def get(self, request, user_id=None):
        if user_id:
            user = self.user_service.get_user(user_id)
            return Response(user, status=status.HTTP_200_OK)
        else:
            details = self.user_service.get_users(request)

            data = formatPaginatedData(details)

            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = self.user_service.create_user(request.data)
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, user_id):
        data = self.user_service.update_user(user_id, request.data, partial=True)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, _, user_id):
        self.user_service.delete_user(user_id)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
