from django.urls import path
from .oauth import *

urlpatterns = [
    path('google/login', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),  
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),

    path('naver/login', naver_login, name='google_login'),
    path('naver/callback/', naver_callback, name='google_callback'),  
    path('naver/login/finish/', NaverLogin.as_view(), name='google_login_todjango'),
    
]