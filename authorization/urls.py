from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_,name='login'),
    path('logout/',views.logout_,name='logout'),
    path('signup/',views.sign_up,name='signup'),
    path('signup/questions/',views.signup_questions,name="questions")

]
