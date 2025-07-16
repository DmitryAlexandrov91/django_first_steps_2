from django.urls import path, include, reverse_lazy
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.conf.urls.static import static
from django.conf import settings

from blog.forms import UserForm


urlpatterns = [
    path('', include('blog.urls')),
    path('posts/', include('blog.urls')),
    path('category/', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
]

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
