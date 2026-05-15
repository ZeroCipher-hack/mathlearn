from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login'), name='home'),
    path('', include('accounts.urls')),
    path('', include('courses.urls')),
    path('', include('tests.urls')),
    path('', include('homework.urls')),
    path('', include('game.urls')),
    path('', include('ratings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
