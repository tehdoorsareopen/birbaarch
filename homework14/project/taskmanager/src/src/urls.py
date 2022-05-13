from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.urls import include, path

urlpatterns = [
    path('', RedirectView.as_view(url='tasks/index/', permanent=False)),
    path('tasks/', include(('taskmanager.urls', 'taskmanager'), namespace='taskmanager')),
    # path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()