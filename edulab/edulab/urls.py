from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exams.urls', namespace='exams')),
    path('auth/', include('users.urls', namespace='auth_users')),
    path('auth/', include('django.contrib.auth.urls')),
]
