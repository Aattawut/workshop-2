from rest_framework.views import exception_handler
# from rest_framework.response import Response

def custom_exception_handler(exc,context):

    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404' : _handle_generic_error,
        'PermissionDenied' : _handle_generic_error,
        'NotAuthenticated' : _handle_authentication_error,
        'NotFound': _handle_notfound,
    }

    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response

def _handle_authentication_error(exc, context, response):

    response.data = {
        "code": "HTTP_401_UNAUTHORIZED",
        "msg": "Authentication credentials were not provided.",
    }
    return response

def _handle_generic_error(exc, context, response):
    response.data = {
         "code": "HTTP_404_NOT_FOUND",
        "msg": "ไม่พบข้อมูล"
    }

    return response

def _handle_notfound(exc, context, response):

    response.data = {
        "code": "HTTP_404_NOT_FOUND",
        "msg": "ไม่พบข้อมูล"
    }

    return response