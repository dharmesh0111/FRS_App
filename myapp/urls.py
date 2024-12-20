
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login_page),
    path('logout',views.logout_page),
#     path('invoices/', views.invoice),
#     path("invoices/statusAPP1/<id>/<code>", views.statusAPP1),
#     path("invoices/statusAPP2/<id>/<code>", views.statusAPP2),
     path('invoices/statusAPP1/<int:id>/<int:code>/', views.statusAPP1, name='statusAPP1'),
     path('invoices/statusAPP2/<int:id>/<int:code>/', views.statusAPP2, name='statusAPP2'),
#     path("invoices/approval2",views.aproval2),
#     path("comment/<id>",views.comment),
     path('invoices/', views.invoice, name='invoices'),  # Make sure 'invoices' matches the reverse lookup
    path('invoices/approval2/', views.aproval2, name='invoices_approval2'),
    path('comment/<int:id>/', views.comment, name='comment'),
    path('subAmtUpdate/<int:id>/', views.subAmt, name='subAmtUpdate'),


        path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='resetPassword.html'), 
         name='password_reset'),
    path('password_reset_done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='resetpassword_done.html'), 
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='resetpassword_confirm.html'), 
         name='password_reset_confirm'),
    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='resetpassword_complate.html'), 
         name='password_reset_complete'),
]
