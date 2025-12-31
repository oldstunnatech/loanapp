from django.shortcuts import render, redirect, get_object_or_404
import numpy as np
import os
import pickle
import joblib
from django.conf import settings
from .forms import LoanPredictionForm
from .models import LoanApplication  # Import your model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import pandas as pd

loan_model = None
encoders = None


def get_loan_model():
    global loan_model
    if loan_model is None:
        model_path = os.path.join(settings.BASE_DIR, "transactionapp", "ML_models", "xgb_model.pkl")
        with open(model_path, "rb") as f:
            loan_model = joblib.load(f)
    return loan_model



def get_encoders():
    global encoders
    if encoders is None:
        encoder_path = os.path.join(settings.BASE_DIR, "transactionapp", "ML_models", "encoders.pkl")
        with open(encoder_path, "rb") as f:
            encoders = pickle.load(f)
    return encoders





HOME_OWNERSHIP_MAP = {
    "Rent": 0,
    "Mortgage": 1,
    "Own": 2,
    "Other": 3,
    }

loan_intent_map = {
    'PERSONAL': 0,
    'EDUCATION': 1,
    'MEDICAL': 2,
    'VENTURE': 3,
    'HOMEIMPROVEMENT': 4,
    'DEBTCONSOLIDATION': 5
}


#function for encoders trained on object strings
def encode(enc, val):
    """
    Safely transform a single value using LabelEncoder or OrdinalEncoder.
    Returns a scalar.
    """
    
    # OrdinalEncoder expects 2D array
    if hasattr(enc, "categories_"):  # OrdinalEncoder
        column_name = enc.feature_names_in_[0]
        df = pd.DataFrame({column_name: [val]})
        return enc.transform(df)[0][0]
    else:  # LabelEncoder
        return enc.transform([val])[0]
    
def encode_label(enc, val):
    return enc.transform([val])[0]  # simple 1D for LabelEncoder



@login_required
def loan_predict_view(request, user_id):
    user = User.objects.get(id=user_id)  # fetch the user
    prediction = None
    probability = None  # initialize

    model = get_loan_model()
    enc = get_encoders()

    if request.method == "POST":
        form = LoanPredictionForm(request.POST)
        
        if form.is_valid():
            gender_val = int(encode(enc["gender"], form.cleaned_data['person_gender']))
            education_val = int(encode(enc["education"], form.cleaned_data['person_education']))
            home_val = HOME_OWNERSHIP_MAP[form.cleaned_data['person_home_ownership']] # Already scalar
            loan_intent_val = loan_intent_map[form.cleaned_data['loan_intent']] # Already scalar
            previous_val = int(encode(enc["previous_loan_defaults_on_file"],form.cleaned_data['previous_loan_defaults_on_file']))

            data = [
                form.cleaned_data['person_age'],
                gender_val,                 # use transformed gender
                education_val,           # ordinal value for education
                form.cleaned_data['person_income'],
                form.cleaned_data['person_emp_exp'],
                home_val,                   # transformed home ownership
                form.cleaned_data['loan_amnt'],
                loan_intent_val,            # transformed loan intent
                form.cleaned_data['loan_int_rate'],
                form.cleaned_data['loan_percent_income'],
                form.cleaned_data['cb_person_cred_hist_length'],
                form.cleaned_data['credit_score'],
                previous_val,               # transformed previous loan defaults
                
                ]
            
            
            # Make prediction
            input_array = np.array([data]) # Creates a shape (1, 13) array
            prediction = int(model.predict(input_array)[0])

            # Optional: if your model provides probability
            try:
                probability = float(model.predict_proba(input_array)[0][1])
            except AttributeError:
                probability = None
                
            LoanApplication.objects.create(
                user=user,
                person_age=form.cleaned_data['person_age'],
                person_gender=form.cleaned_data['person_gender'],
                person_education=form.cleaned_data['person_education'],
                person_income=form.cleaned_data['person_income'],
                person_emp_exp=form.cleaned_data['person_emp_exp'],
                person_home_ownership=form.cleaned_data['person_home_ownership'],
                loan_amnt=form.cleaned_data['loan_amnt'],
                loan_intent=form.cleaned_data['loan_intent'],
                loan_int_rate=form.cleaned_data['loan_int_rate'],
                loan_percent_income=form.cleaned_data['loan_percent_income'],
                cb_person_cred_hist_length=form.cleaned_data['cb_person_cred_hist_length'],
                credit_score=form.cleaned_data['credit_score'],
                previous_loan_defaults_on_file=form.cleaned_data['previous_loan_defaults_on_file'],
                prediction=prediction,
                prediction_probability=probability
            )
            return redirect('loan_result', user_id=user_id)

    else:
        form = LoanPredictionForm()
        # return render(request, "transactionapp/loan_predict.html", {"form":form})
    

    return render(request, "transactionapp/loan_predict.html", {
    "form": form,
    "prediction": prediction,
    "user_id": user_id,  # add this
    "prediction_probability": probability  # optional, if you want to display
})




@login_required
def loan_result_view(request, user_id): 
    
    # 1. SECURITY CHECK: Ensure the requested user_id matches the logged-in user
    # If they don't match, this is a security issue.
    if request.user.id != user_id:
        # Redirect to their own results or deny access
        return redirect('loan_result', user_id=request.user.id) 

    # 2. Fetch the LATEST loan application for the CURRENTLY AUTHENTICATED user
    try:
        application = LoanApplication.objects.filter(user=request.user).latest('id')
    except LoanApplication.DoesNotExist:
        # Redirect the user to the application form if no application is found
        return redirect('loan_predict', user_id=user_id)

    # 3. Customize the status message
    if application.prediction == 1:
        status_message = "Congratulations! Your loan application is successfully **Approved**."
    else:
        # Improved message for the declined case
        status_message = (
            "We regret to inform you that your loan application has been **Denied**. "
            "We will send an email shortly detailing the factors contributing to this decision."
        )
        
    context = {
        'application': application,
        'status_message': status_message,
    }
    
    # Assuming 'transactionapp/loan_result.html' is the correct path
    return render(request, "transactionapp/loan_result.html", context)

# def loan_result_view(request, user_id): 
    
#     # Fetch the LATEST loan application for the given user
#     try:
#         application = LoanApplication.objects.filter(user_id=user_id).latest('id')
#     except LoanApplication.DoesNotExist:
#         # Handle case where no application exists (shouldn't happen immediately after submit)
#         return redirect('loan_predict', user_id=user_id)

#     # You can customize the status message here
#     if application.prediction == 1:
#         status_message = "Congratulations! Your loan application is successfully Approved."
#     else:
#         status_message = "We regret to inform you that your loan application has been Denied. We will inform you in emaili the reason of your declined."
        
#     context = {
#         'application': application,
#         'status_message': status_message,
#         'prediction': application.prediction,
#         'probability': application.prediction_probability,
#     }
    
#     return render(request, "transactionapp/loan_result.html", context)


