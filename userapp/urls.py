from django.urls import path, re_path
from userapp import views as vw 

urlpatterns = [
    path(r'^profile/(?P<userId>\d+)/$', vw.user_profile, name="profile"),
    path(r'^edit_profile/(?P<userId>\d+)/$', vw.edit_profile, name= "edit_profile"),
    path(r'^deactivate_profile/(?P<userId>\d+)/$', vw.deactivate_profile, name="deactivate_profile"),
    path(r'^all_user/(?P<status>\w+)/$', vw.display_users, name="all_user"),
    path(r'^delete_profile/(?P<userId>\d+)/$', vw.delete_profile, name="delete_profile"),
    
]