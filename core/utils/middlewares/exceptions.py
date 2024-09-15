from django.http import JsonResponse
from rest_framework import status

from ..exceptions import AlreadyExistsException, NotFoundException, ValidationException


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.process_exception(request, e)

    def process_exception(self, request, exception):
        if isinstance(exception, NotFoundException):
            return JsonResponse(
                {
                    "status": status.HTTP_404_NOT_FOUND,
                    "data": {},
                    "pagination": {},
                    "success": False,
                    "error": {"message": str(exception)},
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        elif isinstance(exception, AlreadyExistsException):
            return JsonResponse(
                {
                    "status": status.HTTP_409_CONFLICT,
                    "data": {},
                    "pagination": {},
                    "success": False,
                    "error": {"message": str(exception)},
                },
                status=status.HTTP_409_CONFLICT,
            )
        elif isinstance(exception, ValidationException):
            return JsonResponse(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "data": {},
                    "pagination": {},
                    "success": False,
                    "error": {
                        "message": "Validation failed",
                        "details": exception.detail,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            print(exception)
            return JsonResponse(
                {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "data": {},
                    "pagination": {},
                    "success": False,
                    "error": {"message": "Internal server error."},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
