from django.conf.urls import url, include
from django.contrib import admin
from desafio.core.views import home, upload

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^upload/', upload, name='upload'),
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]
