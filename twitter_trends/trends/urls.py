from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('run-script/', views.run_script, name='run_script'),
]
