import logging
import datetime 
from rest_framework.status import HTTP_403_FORBIDDEN
from django.http import JsonResponse
logger = logging.getLogger(__name__)
from django.core import cache
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "AnonymousUser"

        logger.info(f"{datetime.datetime.now()} - User: {user} - Path {request.path}")
        response = self.get_response(request)

        return response
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.block_start = datetime.time(21, 0) # 9pm
        self.block_end = datetime.time(6, 0) # 6am
        
    def __call__(self, request):
        current_time = datetime.datetime.now().time()
        

        if (self.block_start <= current_time) or (current_time < self.block_end):
            return JsonResponse(
                {'error': 'Requests are not allowed between 9 PM and 6 AM'},
                status=HTTP_403_FORBIDDEN
            )
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit_window = 60
        self.max_request = 5
    
    def __call__(self, request):
        if request.method == "POST" and 'messages' in request.path:
            ip = self.get_ip_address(request)
            if not ip:
                return self.get_response(request)
            cache_key = f"rate_limit:{ip}"
            request_times = cache.get(cache_key, [])
            now = time.time()

            request_times = [t for t in request_times if now - t < self.rate_limit_window]

            if len(request_times) >= self.max_request:
                return JsonResponse({
                    "error": "Rate limit exceeded. Max 5 POST requests per minute."
                }, status = 429)
            request_times.append(now)
            cache.set(cache_key, request_times, timeout=self.rate_limit_window)
        return self.get_response(request)
    def get_ip_address(self, request):
        """Extract real client IP address, handling proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

