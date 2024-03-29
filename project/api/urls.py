from django.urls import path
from . import views



urlpatterns = [
    path('',views.main),
    path('files/', views.get_all_files),

]