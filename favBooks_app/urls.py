from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_book', views.add_book),
    path('<int:book_id>', views.view_book),
    path('add_to_fav', views.add_to_fav),
    path('edit', views.edit),
    path('check_destroy/<int:book_id>', views.check_destroy),
    path('destroy', views.destroy),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('user_favorites', views.user_favorites),
]