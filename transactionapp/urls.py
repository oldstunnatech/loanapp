from django.urls import path, re_path
from transactionapp import views as transaction_views
from userapp import views as user_views

urlpatterns = [
    re_path(r'^loan_predict/(?P<user_id>\d+)/', transaction_views.loan_predict_view, name="loan_predict"),
    # path('loan_result/<int:user_id>/', transaction_views.loan_result_view, name='loan_result'),
   
    


]