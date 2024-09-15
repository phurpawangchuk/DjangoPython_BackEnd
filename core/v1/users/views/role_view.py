from injector import Injector
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ....utils.helpers.responses import CustomRenderer, formatPaginatedData
from ....utils.modules.app_module import AppModule
from ..services import RoleService

injector = Injector([AppModule()])


class RoleView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [CustomRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role_service = injector.get(RoleService)

    def get(self, request, role_id=None):
        if role_id:
            role = self.role_service.get_role(role_id)
            return Response(role, status=status.HTTP_200_OK)
        else:
            details = self.role_service.get_roles(request)
            data = formatPaginatedData(details)

            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = self.role_service.create_role(request.data)
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, role_id):
        data = self.role_service.update_role(role_id, request.data, partial=True)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, _, role_id):
        self.role_service.delete_role(role_id)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
