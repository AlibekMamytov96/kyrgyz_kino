from django.urls import path

from .import views
from .views import *

urlpatterns = [
    path('', views.MoviesView.as_view(), name='media'),
    path('create/', views.CreateMovieView.as_view(), name='create_movie'),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category_list'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("movie/<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("update/<str:slug>/", views.UpdateMovieView.as_view(), name="update_movie"),
    path("delete/<str:slug>/", views.DeleteMovieView.as_view(), name="delete_movie"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),

    path('search/', views.SearchMovieView.as_view(), name='search'),
    path('favourites/<int:id>/', views.add_to_favourites, name='add_to_favourites'),
    path('account/favourites/', views.favourites_list, name='favourites_list'),
    path('like/<int:pk>/', views.like_movie, name='like_movie'),
]