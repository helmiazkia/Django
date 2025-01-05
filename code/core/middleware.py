import logging

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        self.logger.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        self.logger.info(f"Response: {response.status_code}")
        return response
