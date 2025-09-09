from django.urls import path

from tenancy import views

urlpatterns = [
    # General 
    path('dashboard/', views.dashboard, name='tenancy_dashboard'),
    path('details/', views.details, name='tenancy_details'),
    path('history/', views.history, name='tenancy_history'),
    
    # Subscription
    path('standing/', views.standing, name='tenancy_standing'),
    path('trial/', views.trial, name='tenancy_trial'),
    path('subscriptions/', views.subscriptions, name='tenancy_subscriptions'),
    path('subscribe/', views.subscribe, name='tenancy_subscribe'),
    path('sub-cancel/', views.sub_cancel, name='tenancy_sub_cancel'),
    path('plan-select/', views.plan_select, name='tenancy_plan_select'),
    path('sub-upgrade/', views.sub_upgrade, name='tenancy_sub_upgrade'),

    # Users
    path('users/', views.users, name='tenancy_users'),
    path('add_user/', views.add_user, name='tenancy_add_user'),
    path("users/<str:user_id>/disable/", views.disable_user, name="disable_user"),
    path("users/<str:user_id>/enable/", views.enable_user, name="enable_user"),
    path("users/<str:user_id>/adminize/", views.adminize_user, name="adminize_user"),
    path("users/<str:user_id>/disadminize/", views.disadminize_user, name="disadminize_user"),
    path("users/<str:user_id>/delete/", views.delete_user, name="delete_user"),

    # Orders and payments
    path('order/', views.order, name='tenancy_order'),
    path('orders/', views.orders, name='tenancy_orders'),
    path('orders/<str:order_id>/delete', views.delete_order, name='tenancy_delete_order'),
    path('orders/<str:order_id>/details', views.order_details, name='tenancy_order_details'),
    path('order-payments/<str:order_id>', views.order_payments, name='tenancy_order_payments'),
    path('order-payments/<str:order_id>/add', views.add_order_payment, name='tenancy_add_order_payment'),
    path('order-payment/<str:payment_id>/delete', views.delete_order_payment, name='tenancy_delete_order_payment'),
    path('order-payment/<str:payment_id>/edit', views.edit_order_payment, name='tenancy_edit_order_payment'),

    # path('edit_order_payment/<str:payment_id>', views.order_payment_form, name='tenancy_edit_order_payment'),
]
