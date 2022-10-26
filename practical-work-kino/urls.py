from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from decorator_include import decorator_include
from django.contrib.auth.decorators import user_passes_test
from . import settings

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += i18n_patterns(
    path('admin_cms/', decorator_include(user_passes_test(lambda u: u.is_superuser), 'admin_cms.urls')),
    path('', include('cinema.urls')),
    path('event/', include('event.urls')),
    path('page/', include('page.urls')),
    path('movie/', include('movie.urls')),
    # path('banner/', include('banner.urls')),
    path('user/', include('user.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)