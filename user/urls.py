from django.urls import path
from .oauth import *

urlpatterns = [
    path('google/login', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),  
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),

    path('naver/login', naver_login, name='naver_login'),
    path('naver/callback/', naver_callback, name='naver_callback'),  
    path('naver/login/finish/', NaverLogin.as_view(), name='naver_login_todjango'),   

    path('kakao/login', kakao_login, name='kakao_login'),
    path('kakao/callback/', kakao_callback, name='kakao_callback'),  
    path('kakao/login/finish/', KakaoLogin.as_view(), name='kakao_login_todjango'),   
]