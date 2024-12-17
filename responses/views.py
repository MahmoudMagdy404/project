from django.shortcuts import render, redirect
from django.contrib import messages
from .authentication import login_required
from .services.auth_service import authenticate_agent
from .services.firebase_service import save_response_data, get_all_responses

def login_view(request):
    """Handle agent login"""
    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        password = request.POST.get('password')
        
        try:
            is_authenticated, role = authenticate_agent(agent_id, password)
            if is_authenticated:
                request.session['agent_id'] = agent_id
                request.session['role'] = role
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except Exception as e:
            messages.error(request, 'Login failed. Please try again.')
            print(f"Login error: {e}")
    
    return render(request, 'responses/login.html')

def logout_view(request):
    """Handle agent logout"""
    request.session.flush()
    return redirect('login')

@login_required
def dashboard_view(request):
    """Display role-specific dashboard"""
    role = request.session.get('role')
    agent_id = request.session.get('agent_id')
    
    if role == 'TL':
        # Fetch all responses for team leader view
        responses = get_all_responses()
        return render(request, 'responses/team_leader_dashboard.html', {
            'agent_id': agent_id,
            'responses': responses
        })
    else:
        # Regular agent dashboard
        return render(request, 'responses/agent_dashboard.html', {
            'agent_id': agent_id
        })

@login_required
def submit_response(request):
    """Handle response submission"""
    agent_id = request.session.get('agent_id')
    
    if request.method == 'POST':
        try:
            response_data = {
                'agent_id': agent_id,  # Automatically use logged-in agent's ID
                'team_leader': request.POST.get('team_leader'),
                'agent_name': agent_id,  # Use the same agent ID
                'sns_result': request.POST.get('sns_result'),
                'requested_device': request.POST.get('requested_device'),
                'pt_full_name': request.POST.get('pt_full_name'),
                'provider': request.POST.get('provider'),
                'pt_phone_number': request.POST.get('pt_phone_number'),
                'medicare_id': request.POST.get('medicare_id'),
                'date_of_birth': request.POST.get('date_of_birth'),
                'pt_full_address': request.POST.get('pt_full_address'),
                'height': request.POST.get('height'),
                'weight': request.POST.get('weight'),
                'waist_size': request.POST.get('waist_size'),
                'shoe_size': request.POST.get('shoe_size'),
                'primary_doctor_aware': request.POST.get('primary_doctor_aware') == 'on',
                'last_seen_doctor': request.POST.get('last_seen_doctor'),
                'diabetic': request.POST.get('diabetic') == 'on',
                'relatives_with_cancer': request.POST.get('relatives_with_cancer') == 'on',
                'plan': request.POST.get('plan'),
            }
            
            save_response_data(response_data)
            messages.success(request, 'Response submitted successfully')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, 'Failed to submit response. Please try again.')
            print(f"Response submission error: {e}")
        
    return render(request, 'responses/submit_response.html', {
        'agent_id': agent_id
    })