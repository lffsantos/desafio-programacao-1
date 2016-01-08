from django.conf.urls import url
from django.contrib import admin
from desafio.core.views import home, upload

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^upload/', upload, name='upload'),
    url(r'^admin/', admin.site.urls),
]
