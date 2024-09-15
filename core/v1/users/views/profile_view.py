from injector import Injector
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ....utils.helpers.responses import CustomRenderer
from ....utils.modules.app_module import AppModule
from ..services import ProfileService

injector = Injector([AppModule()])


class ProfileView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [CustomRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.profile_service = injector.get(ProfileService)

    def get(self, _, user_id):
        profile = self.profile_service.get_profile(user_id)
        return Response(profile, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        data = self.profile_service.create_profile(user_id, request.data)
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, user_id):
        data = self.profile_service.update_profile(user_id, request.data)
        return Response(data, status=status.HTTP_200_OK)
