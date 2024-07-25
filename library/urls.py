from django.urls import path
from . import views 
from . import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('manage_folder/<int:folder_id>/', views.manage_folder, name='manage_folder'),
    path('favorites/', views.favorites, name='favorites'),
    path('manage_folder/', views.manage_folder, name='manage_folder'),
    path('manage_folder/<int:folder_id>/', views.manage_folder, name='manage_folder_edit'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('delete_music/<int:music_id>/', views.delete_music, name='delete_music'),
    path('favorites/', views.favorites, name='favorites'),
    path('add-folder-to-favorites/<int:folder_id>/', views.add_folder_to_favorites, name='add_folder_to_favorites'),
]


