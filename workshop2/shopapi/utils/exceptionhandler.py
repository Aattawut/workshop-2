

def custom_exception_handler(exc,context):

    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404' : _handle_generic_error,
        'PermissionDenied' : _handle_generic_error,
        'NotAuthenticated' : _handle_authentication_error
    }

def _handle_generic_error(exc, context, response):
    re