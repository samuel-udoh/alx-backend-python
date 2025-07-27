import logging
from datetime import datetime, time
from rest_framework.status import HTTP_403_FORBIDDEN
from django.http import JsonResponse
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"

        logger.info(f"{datetime.now()} - User: {user} - Path {request.path}")
        response = self.get_response(request)

        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.block_start = time(21, 0) # 9pm
        self.block_end = time(6, 0) # 6am
        
    def __call__(self, request):
        current_time = datetime.now().time()
        

        if (self.block_start <= current_time) or (current_time < self.block_end):
            return JsonResponse(
                {'error': 'Requests are not allowed between 9 PM and 6 AM'},
                status=HTTP_403_FORBIDDEN
            )
        return self.get_response(request)
