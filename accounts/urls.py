from django.urls import path
#from .views import RoleLoginView, RoleLogoutView, post_login, login_options
from . import views

from django.contrib.auth import views as auth_views

urlpatterns=[
 path('login/',  views.RoleLoginView.as_view(), name='login'),
 path('logout/',  views.RoleLogoutView.as_view(), name='logout'),

 path('post-login',  views.post_login, name='post_login'),
 path('auth/choose/',  views.login_options, name='login_options'),

 path('signup/scuola-full/', views.signup_scuola_full, name='signup_scuola_full'),
 path("signup/ente-full/",   views.signup_ente_full,   name="signup_ente_full"),  # 
 
 path('activate/<str:token>/', views.activate, name='activate'),

 path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
 path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
 path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
 path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
