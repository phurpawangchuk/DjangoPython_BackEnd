from injector import Injector
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ....utils.helpers.responses import CustomRenderer, formatPaginatedData
from ....utils.modules.app_module import AppModule
from ..services import PostService

injector = Injector([AppModule()])

from django.core.paginator import Paginator


class PostView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_service = injector.get(PostService)

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [IsAuthenticated()]

    def get(self, request, post_id=None):
        if request.path.endswith("/history/"):
            if post_id:
                post_history = self.post_service.get_post_history(post_id, request)
                response_data = formatPaginatedData(post_history)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "Post ID is required for history."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        elif post_id:
            post = self.post_service.get_post(post_id)
            return Response(post, status=status.HTTP_200_OK)
        else:
            details = self.post_service.get_posts(request)
            response = formatPaginatedData(details)
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data = self.post_service.create_post(request.data)
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, post_id):
        data = self.post_service.update_post(post_id, request.data, partial=True)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, _, post_id):
        self.post_service.delete_post(post_id)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
