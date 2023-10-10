from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('display-rankings/', views.display_rankings, name='display_rankings'),
    path('add-match/', views.add_match, name='add_match'),
    path('edit-match/<int:match_id>/', views.edit_match, name='edit_match'),
    path('delete-match/<int:match_id>/', views.delete_match, name='delete_match'),
    path('match-list/', views.match_list, name='match_list')
]