# encoding: utf-8

'''📜 Dicominator site policy: URL patterns.'''


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
# from jpl.labcas.dicominator.theme.urls import urlpatterns as theme_urlpatterns
# from jpl.labcas.dicominator.tags.urls import urlpatterns as usermgmt_urlpatterns


# urlpatterns = usermgmt_urlpatterns + theme_urlpatterns + [
urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
]

# Note: we wouldn't normally want to serve static files or media out of the `urlpatterns` listed
# here. This means that the Django app is doing unnecessary work. However, in order to Dockerize
# this app, it does make sense to at laeast provide a fallback for Django (+ wsgi + gunicorn) to do
# the work in order to be completely containerized.
#
# So we do include the static files and media URL patterns to support this. However, in an optimal
# deployment, the ALB (or Nginx or Apache HTTPD or whatever) would intercept /static and /media URLs
# and serve them directly out of the host filesystem.

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ModuleNotFoundError:
        pass
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
