from django.urls import path

from tenancy import views

urlpatterns = [
    path('summary/', views.summary, name='tenancy_summary'),
    path('order/', views.order, name='tenancy_order'),
    path('trial/', views.trial, name='tenancy_trial'),
    path('dashboard/', views.dashboard, name='tenancy_dashboard'),
    path('details/', views.details, name='tenancy_details'),
    path('history/', views.history, name='tenancy_history'),
    path('sub-cancel/', views.sub_cancel, name='tenancy_sub_cancel'),
    path('subscribe/', views.subscribe, name='tenancy_subscribe'),
    path('sub-upgrade/', views.sub_upgrade, name='tenancy_sub_upgrade'),
    path('users/', views.users, name='tenancy_users'),
    path('add_user/', views.add_user, name='tenancy_add_user'),
    path("users/<str:user_id>/disable/", views.disable_user, name="disable_user"),
    path("users/<str:user_id>/enable/", views.enable_user, name="enable_user"),
    path("users/<str:user_id>/adminize/", views.adminize_user, name="adminize_user"),
    path("users/<str:user_id>/disadminize/", views.disadminize_user, name="disadminize_user"),
    path("users/<str:user_id>/delete/", views.delete_user, name="delete_user"),
    # tenancy_orders #
    path('orders/', views.orders, name='tenancy_orders'),
    path('order-payments/<str:order_id>', views.order_payments, name='tenancy_order_payments'),
    path('order-payments/<str:order_id>/add', views.add_order_payment, name='tenancy_add_order_payment'),
    path('order-payment/<str:payment_id>/delete', views.delete_order_payment, name='tenancy_delete_order_payment'),
    path('order-payment/<str:payment_id>/edit', views.edit_order_payment, name='tenancy_edit_order_payment'),

    # path('edit_order_payment/<str:payment_id>', views.order_payment_form, name='tenancy_edit_order_payment'),
]
