from rest_framework import renderers
from rest_framework import status as status_code


class CustomRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"] if renderer_context else None
        status = response.status_code if response else None
        success = status in range(
            status_code.HTTP_200_OK, status_code.HTTP_300_MULTIPLE_CHOICES
        )

        main_data = data.get("list", data)
        pagination = data.get("pagination", {})

        formatted_data = {
            "status": status,
            "data": main_data,
            "success": success,
            "error": {},
        }

        if pagination:
            formatted_data["pagination"] = pagination

        return super().render(formatted_data, accepted_media_type, renderer_context)


def formatPaginatedData(details):
    list_data, total, num_pages, current_page = details

    return {
        "list": list_data,
        "pagination": {
            "total": total,
            "num_pages": num_pages,
            "current_page": current_page,
            "count": len(list_data),
        },
    }
