"""core URL Configuration

"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("home.urls")),
    path("user/", include("user.urls")),
    path("chat/", include("chat.urls")),
    path('', include('blog.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
