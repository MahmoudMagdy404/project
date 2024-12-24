from django import forms

class UserForm(forms.Form):
    agent_id = forms.CharField(label="Agent ID", max_length=50, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(label="Role", choices=[('TL', 'Team Leader'), ('agent', 'Agent')], required=True)
