"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/clearcache/', include('banners.urls')),
    path('admin/', admin.site.urls),
    path('', include('customers.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('goods/', include('goods.urls')),
    path('banners/', include('banners.urls')),
    path('customers/', include('customers.urls')),
    path('', include('app_shop.urls')),
    path('orders/', include('orders.urls')),
    path('sale/', include('discounts.urls')),
    path('import/', include('data_import.urls')),
    path('i18n', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

