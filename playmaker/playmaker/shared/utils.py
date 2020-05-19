from django.http import HttpResponse
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class NotLoggedInException(APIException):
    status_code = 401
    default_detail = {"Reason": "Not logged in."}


def make_iterable(data):
    if type(data) == list:
        return data
    else:
        return [data]


# TODO not utilized yet
def exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotLoggedInException):
        return HttpResponse("Not logged in.", status=401)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


def as_views(items, serializer):
    return [serializer(instance=item).data for item in items]