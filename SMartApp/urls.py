"""
Definition of urls for SMartApp.
"""

from datetime import datetime
from django.urls import path,include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
import debug_toolbar

urlpatterns = [

    path('__debug__/', include(debug_toolbar.urls)),

    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    # path('oauth2/', include('django_auth_adfs.urls')), # django-auth-adfs
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # django-oauth-toolkit
    path('admin/', admin.site.urls),

    path('', include('app.urls')),

    path('login/',
         LoginView.as_view
             (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
