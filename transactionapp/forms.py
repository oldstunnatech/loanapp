from django import forms
from .models import LoanApplication

class LoanPredictionForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'person_gender',
            'person_education',
            'person_home_ownership',
            'loan_intent',
            'previous_loan_defaults_on_file',
            'person_age',
            'person_income',
            'person_emp_exp',
            'loan_amnt',
            'loan_int_rate',
            'loan_percent_income',
            'cb_person_cred_hist_length',
            'credit_score'
            ]

        widgets = {'person_gender': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Select Gender')] + list(LoanApplication.GENDER_CHOICES)),
                   'person_education': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Select Education')] + list(LoanApplication.EDUCATION_CHOICES)),
'person_home_ownership': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Select Home Ownership')] + list(LoanApplication.HOME_OWNERSHIP_CHOICES)),
'loan_intent': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Select Loan Intent')] + list(LoanApplication.LOAN_INTENT_CHOICES)),
'previous_loan_defaults_on_file': forms.Select(attrs={'class': 'form-select'}, choices=[('', 'Select Option')] + list(LoanApplication.PREVIOUS_DEFAULTS_CHOICES)),
'person_age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),
'person_income': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Income'}),
'person_emp_exp': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Employment Experience in years'}),
'loan_amnt': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Loan Amount'}),
'loan_int_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Interest Rate'}),
'loan_percent_income': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Loan as % of Income'}),
'cb_person_cred_hist_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Credit History Length'}),
'credit_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Credit Score'}),
}
