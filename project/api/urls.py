from django.urls import path
from . import views



urlpatterns = [
    path('',views.main),
    path('files/', views.get_all_files),
    path('pdf', views.convert_pngs_to_pdf),
    path('backup', views.backup_files ),

]