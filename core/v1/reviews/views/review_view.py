from injector import Injector
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ....utils.helpers.responses import CustomRenderer, formatPaginatedData
from ....utils.modules.app_module import AppModule
from ..services.review_service import ReviewService

injector = Injector([AppModule()])


class ReviewView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [CustomRenderer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.review_service = injector.get(ReviewService)

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    def get(self, request, review_id=None):
        if review_id:
            review = self.review_service.get_review(review_id)
            return Response(review, status=status.HTTP_200_OK)
        else:
            details = self.review_service.get_reviews(request)
            data = formatPaginatedData(details)

            return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = self.review_service.create_review(request.data)
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, review_id):
        data = self.review_service.update_review(review_id, request.data)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, _, review_id):
        self.review_service.delete_review(review_id)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
