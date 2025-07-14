from django.contrib import admin
from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns
# from django.conf.urls.static import static
# from django.conf import settings


urlpatterns = i18n_patterns(
    path('', include('base.urls')),
    path('admin/', admin.site.urls),
)


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)