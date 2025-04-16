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
]

# reports
urlpatterns += [
    path('reports/', views.ReportView.as_view(), name='reports'),
    path('verify-reports/', views.VerifyReportView.as_view(), name='verify_report'),
    path('download-reports/', views.DownloadReportsView.as_view(), name='download_reports'),
]

# schools
urlpatterns += [
    path('schools/', views.SchoolsView.as_view(), name='schools'),
    path('delete-school/', views.DeleteSchoolView.as_view(), name='delete_school'),
    path('create-update-school/', views.CreateUpdateSchoolView.as_view(), name='create_update_school'),
    path('download-schools/', views.DownloadSchoolsView.as_view(), name='download_schools'),
]


# users
urlpatterns += [
    path('users/', views.UsersView.as_view(), name='users'),
    path('user-details/', views.UserDetailsView.as_view(), name='user_details'),
    path('create-update-user/', views.CreateUpdateUser.as_view(), name='create_update_user'), #noqa
    path('update-user-pic/', views.UpdateUserProfilePicView.as_view(), name='update_profile_pic'), #noqa
    path('download-users/', views.DownloadUsersView.as_view(), name='download_users'), #noqa

    path('add-user-to-group/', views.AddUserToGroupsView.as_view(), name='add_user_to_group'), #noqa
    path('add-perm-to-user/', views.AddPermsToUserView.as_view(), name='add_perm_to_user'), #noqa
]
