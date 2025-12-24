from django.shortcuts import redirect


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def proccess_request(request):
        pass
    
    def proccess_response(request,response):
        pass
    
    def __call__(self, request):
        # before response
        print(f"Request Method: {request.method}, Request Path: {request.path}")

        response = self.get_response(request)
        print(f"Response Status Code: {response.status_code}")

        # after response
        return response

# fullNameAge


class AuthCheckMiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response
        
    def __call__(self,request):
        
        protected_routes = ["/", "/admin/"]
        
        if not request.user.is_authenticated and request.path in protected_routes:
            return redirect("/user/login/")
        
        response = self.get_response(request)
        
        return response

        

