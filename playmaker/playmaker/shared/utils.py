from django.http import HttpResponse
from rest_framework.views import exception_handler


class NotLoggedInException(Exception):
    pass


def make_iterable(data):
    if type(data) == list:
        return data
    else:
        return [data]


def exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotLoggedInException):
        return HttpResponse("Not logged in.", status=401)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response