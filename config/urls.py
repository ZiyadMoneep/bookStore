"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
                  # Admin
                  path('admin/', admin.site.urls),

                    #API
                  path('api/', include('api.urls')),
                  # User management
                  # path('accounts/', include('django.contrib.auth.urls')),
                  # Custom User management
                  # path('accounts/', include('accounts.urls')),

                  # Django-allauth
                  path('accounts/', include('allauth.urls')),

                  # Pages app
                  path('', include('pages.urls')),

                  # Books app
                  path('books/', include('books.urls')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                      path("__reload__/", include("django_browser_reload.urls")),
                  ] + urlpatterns
