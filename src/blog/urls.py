
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import(
    login_view,
    register_view,
    logout_view,
)
from home.views import feedback


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register_view, name = "register_view"),
    url(r'^login/$', login_view, name = "login"),
    url(r'^logout/$', logout_view, name = "logout"),
    url(r'^feedback/$', feedback, name = "feedback"),
    url(r'^', include("posts.urls", namespace = 'posts')),
    
    #url(r'^posts/$', <appname>.views.<function_name>),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)