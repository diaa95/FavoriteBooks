from django.urls import path
from . import views, models

urlpatterns = [
    path('', views.index),
    path("register", views.register),
    path('log_in', views.log_in),
    path('log_out', views.log_out),
    path('user_page/<user_id>', views.user_page),
    path("success/<user_id>", views.success),
    path("add_book/<user_id>", views.add_book),
    path("book_details/<user_id>/<book_id>", views.book_details),
    path("edit/<book_id>/<user_id>", views.edit),
    path("display/<book_id>/<user_id>", views.display),
    path("add_fav/<book_id>/<user_id>", views.add_fav),
    path('UnFavorite/<book_id>/<user_id>', views.unfavorite),
    path('books/<book_id>/<user_id>/update', views.update),
    path('books/<book_id>/<user_id>/destroy', views.destroy),
]