from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('habits.urls')),
    path('api/', include('habits.api.urls')),
    path('', include('reminders.urls'))

]
