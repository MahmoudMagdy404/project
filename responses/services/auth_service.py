"""
Authentication service layer
"""
from .firebase_service import get_agent_by_id

def authenticate_agent(agent_id, password):
    """
    Authenticate agent using Firebase and return authentication status and role
    Returns tuple (is_authenticated: bool, role: str)
    """
    try:
        agent_data = get_agent_by_id(agent_id)
        if agent_data and agent_data.get('password') == password:
            # Check for TL or agent role
            role = agent_data.get('role', 'agent')
            if role not in ['TL', 'agent']:
                return False, None
            return True, role
        return False, None
    except Exception as e:
        print(f"Authentication error: {e}")
        return False, None