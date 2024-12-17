from django.db import models
from django.contrib.auth.models import User

class ResponseData(models.Model):
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_leader_responses')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_responses')
    comment = models.TextField(blank=True)
    sns_result = models.TextField()
    provider_good_for = models.CharField(max_length=255)
    requested_device = models.CharField(max_length=255)
    
    # Patient Information
    patient_name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    medicare_id = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    full_address = models.TextField()
    
    # Physical Characteristics
    height = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    waist_size = models.CharField(max_length=50)
    shoe_size = models.CharField(max_length=50)
    
    # Medical Questions
    doctor_aware_of_pain = models.BooleanField()
    last_doctor_visit = models.CharField(max_length=255)
    is_diabetic = models.BooleanField()
    family_cancer_history = models.BooleanField()
    
    # Additional Information
    timestamp = models.DateTimeField(auto_now_add=True)
    poa_name = models.CharField(max_length=255, blank=True)
    plan = models.CharField(max_length=100)
    employment_status = models.CharField(max_length=50, choices=[('PT', 'Part Time'), ('FT', 'Full Time')])
    
    # Medical Conditions
    joint_flexibility_issues = models.BooleanField()
    joint_numbness = models.BooleanField()
    skin_diseases = models.BooleanField()
    psoriasis_diagnosis = models.BooleanField()
    limb_swelling = models.BooleanField()
    
    def __str__(self):
        return f"Response for {self.patient_name} - {self.timestamp}"