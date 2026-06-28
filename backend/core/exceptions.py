import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger()

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        logger.error(f"API Exception: {exc.__class__.__name__} - {str(exc)}")
        response.data = {
            'error': True,
            'message': str(response.data.get('detail', response.data)),
            'status_code': response.status_code,
        }
    else:
        logger.error(f"Unhandled Exception: {exc.__class__.__name__} - {str(exc)}", exc_info=True)
        response = Response(
            {
                'error': True,
                'message': 'Internal server error. Please try again later.',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response