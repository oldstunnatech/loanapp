from django.db import models
from django.contrib.auth.models import User 
# Create your models here.




class LoanApplication(models.Model):


    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]

    EDUCATION_CHOICES = [
        ('High School', 'High School'),
        ('Associate', 'Associate'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('Doctorate', 'Doctorate'),
        ]

    HOME_OWNERSHIP_CHOICES = [
        ('Rent', 'Rent'), 
        ('Own', 'Own'), 
        ('Mortgage', 'Mortgage')
        ]

    LOAN_INTENT_CHOICES = [
        ('PERSONAL', 'PERSONAL'), 
        ('EDUCATION', 'EDUCATION'), 
        ('MEDICAL', 'MEDICAL'),
        ('VENTURE', 'VENTURE'), 
        ('HOMEIMPROVEMENT', 'HOMEIMPROVEMENT'),
        ('DEBTCONSOLIDATION', 'DEBTCONSOLIDATION'), 
        ]

    PREVIOUS_DEFAULTS_CHOICES = [
        ('Yes', 'Yes'), 
        ('No', 'No')
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications', null=True)
    person_age = models.IntegerField()
    person_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    person_education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    person_income = models.FloatField()
    person_emp_exp = models.FloatField()
    person_home_ownership = models.CharField(max_length=10, choices=HOME_OWNERSHIP_CHOICES)
    # Loan Information
    loan_amnt = models.FloatField()
    loan_intent = models.CharField(max_length=20, choices=LOAN_INTENT_CHOICES)
    loan_int_rate = models.FloatField()
    loan_percent_income = models.FloatField()

    # Credit Information
    cb_person_cred_hist_length = models.FloatField()
    credit_score = models.FloatField()
    previous_loan_defaults_on_file = models.CharField(max_length=3, choices=PREVIOUS_DEFAULTS_CHOICES)

    # Prediction Result
    prediction = models.CharField(max_length=20, blank=True, null=True)
    prediction_probability = models.FloatField(blank=True, null=True)

    # Timestamp
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan Application #{self.id} - Age {self.person_age}, Prediction: {self.prediction}"