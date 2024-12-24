from django.shortcuts import render, redirect
from django.contrib import messages
from .authentication import login_required
from .services.auth_service import authenticate_agent
from .services.firebase_service import save_response_data, get_all_responses
from responses.services.forms import UserForm
from .services.firebase_service import add_user_to_firestore
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.firebase_service import generate_new_user


@csrf_exempt
def generate_user(request):
    """Handle user generation."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        role = request.POST.get('role', '').strip()

        # Debugging: Log inputs
        print(f"Received data: name={name}, role={role}")

        # Validate input
        if not name or not role:
            return JsonResponse({'error': 'Name and Role are required'}, status=400)

        try:
            agent_id, password = generate_new_user(name, role)
            return JsonResponse({'agent_id': agent_id, 'password': password})
        except Exception as e:
            print(f"Error in generate_user: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def add_user_view(request):
    """View to add a new user to Firestore"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            agent_id = form.cleaned_data['agent_id'].strip()
            password = form.cleaned_data['password'].strip()
            role = form.cleaned_data['role']

            try:
                add_user_to_firestore(agent_id, password, role)
                messages.success(request, f"User '{agent_id}' added successfully.")
                return redirect('add_user')  # Redirect to the same form page
            except Exception as e:
                messages.error(request, f"Error adding user: {e}")
    else:
        form = UserForm()

    return render(request, 'responses/add_user.html', {'form': form})
def login_view(request):
    """Handle agent login."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()  # Use name instead of agent_id
        password = request.POST.get('password', '').strip()

        try:
            is_authenticated, role, agent_id = authenticate_agent(name, password)
            print(f"Authentication result: is_authenticated={is_authenticated}, role={role}, id={agent_id}")  # Debugging

            if is_authenticated:
                # Store role, name, and agent_id in the session
                request.session['agent_name'] = name
                request.session['role'] = role
                request.session['agent_id'] = agent_id  # Add agent's ID to the session
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
    role = request.session.get('role')
    agent_name = request.session.get('agent_name')  # Fetch agent's name from the session
    agent_id = request.session.get('agent_id')  # Fetch agent's ID

    print(f"Accessing Dashboard: Agent Name = {agent_name}, Agent ID = {agent_id}, Role = {role}")

    if role == 'TL':
        responses = get_all_responses()
        return render(request, 'responses/team_leader_dashboard.html', {
            'agent_name': agent_name,
            'agent_id': agent_id,
            'responses': responses
        })
    else:
        return render(request, 'responses/agent_dashboard.html', {
            'agent_name': agent_name,
            'agent_id': agent_id
        })



@login_required
def submit_response(request):
    """Handle response submission"""
    agent_id = request.session.get('agent_id')
    agent_name = request.session.get("name")

    if request.method == 'POST':
        try:
            response_data = {
                'agent_id': agent_id,  # Automatically use logged-in agent's ID
                'team_leader': request.POST.get('team_leader'),
                'agent_name': agent_name,  # Use the same agent ID
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