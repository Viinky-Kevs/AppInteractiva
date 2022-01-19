from django.contrib import admin
from django.urls import path, include
from AppWeb import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.index, name = 'home'),
	path('registeruser/', views.register_user, name = 'registration'),
	path('interactivemap/', views.home.as_view(), name = 'map'),
	path('group/', views.group, name = 'group'),
	path('upload/', views.upload, name = 'upload'),
	path('interactivemap/configuration/', views.config, name = 'config'),
	path('analysis/', views.analysis, name='analysis'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
