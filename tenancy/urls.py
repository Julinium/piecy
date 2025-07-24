from django.urls import path

from tenancy import views

urlpatterns = [
    path('summary/', views.summary, name='tenancy_summary'),
    path('trial/', views.trial, name='tenancy_trial'),
    path('dashboard/', views.dashboard, name='tenancy_dashboard'),
    path('details/', views.details, name='tenancy_details'),
    path('history/', views.history, name='tenancy_history'),
    path('sub-cancel/', views.sub_cancel, name='tenancy_sub_cancel'),
    path('sub-renew/', views.sub_renew, name='tenancy_sub_renew'),
    path('sub-upgrade/', views.sub_upgrade, name='tenancy_sub_upgrade'),
    path('users/', views.users, name='tenancy_users'),
]
