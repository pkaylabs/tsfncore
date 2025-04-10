from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

# dashboard urls
urlpatterns += [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]


# profile settings
urlpatterns += [
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/preference', views.PreferenceSettingsView.as_view(), name='prefered_settings'), #noqa
    path('settings/password-reset', views.PasswordResetView.as_view(), name='password_reset'), #noqa
    path('settings/change-profile-pic', views.ChangeProfilePicView.as_view(), name='change_profile_pic'), #noqa
    # path('profile/', views.UserProfileView.as_view(), name='profile'),
]