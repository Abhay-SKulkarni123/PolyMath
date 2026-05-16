from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_message = 'An error occurred.'

        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_message = str(response.data['detail'])
            else:
                messages = []
                for field, errors in response.data.items():
                    if isinstance(errors, list):
                        messages.append(f'{field}: {errors[0]}')
                    else:
                        messages.append(str(errors))
                error_message = ' | '.join(messages)

        elif isinstance(response.data, list):
            error_message = str(response.data[0])

        response.data = {
            'error': True,
            'message': error_message,
            'status_code': response.status_code,
        }

    return response