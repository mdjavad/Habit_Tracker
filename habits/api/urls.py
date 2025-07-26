from django.urls import path
from . import views 


urlpatterns = [
    path('', views.getRoutes),
    path('habits/', views.getHabits)
]
