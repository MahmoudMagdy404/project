from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .services.firebase_service import get_agent_by_id  # Correct import

def authenticate_agent(agent_id, password):
    """Authenticate agent using Firebase"""
    agent_data = get_agent_by_id(agent_id)
    if agent_data and agent_data.get('password') == password:
        return True
    return False

def login_required(view_func):
    """Custom decorator for login requirement"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('agent_id'):
            messages.error(request, 'Please login first')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
