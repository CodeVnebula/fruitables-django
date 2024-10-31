from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class CustomSessionMiddleware(MiddlewareMixin):
    SESSION_AGE = 60
    
    def process_request(self, request):
        if 'last_activity' not in request.session:
            request.session['last_activity'] = timezone.now().timestamp()
            
        current_time = timezone.now().timestamp()
        last_activity_time = request.session['last_activity']
    
        if current_time - last_activity_time > self.SESSION_AGE:
            request.session.flush()  
            return None 
        request.session['last_activity'] = current_time
        request.session.modified = True
