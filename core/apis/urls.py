from django.urls import path
from . import views

app_name = 'apis'

urlpatterns = [
    path('', views.PingAPI.as_view(), name='ping'),
]

# auth and user api endpoints
urlpatterns += [
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('logout/', views.LogoutAPI.as_view(), name='logout'),
    path('userprofile/', views.UserProfileAPIView.as_view(), name='userprofile'),
    path('verifyotp/', views.VerifyOTPAPI.as_view(), name='verifyotp'),
    path('changepassword/', views.ChangePasswordAPIView.as_view(), name='changepassword'),
    path('resetpassword/', views.ResetPasswordAPIView.as_view(), name='resetpassword'),
]


# reports api endpoints
urlpatterns += [
    path('reports/', views.SubmittedReportsAPIView.as_view(), name='reports'),
]