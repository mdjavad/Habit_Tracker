# decorators.py
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import User

def role_required(*allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect('login')

            user = User.objects.get(id=user_id)

            if user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Access Denied: Role not allowed.")
        return wrapper
    return decorator
