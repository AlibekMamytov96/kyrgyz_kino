from django.urls import path

from .import views


urlpatterns = [
    path('', views.MoviesView.as_view()),
    path('create/', views.CreateMovieView.as_view(), name='create_movie'),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("update/<str:slug>/", views.UpdateMovieView.as_view(), name="update_movie"),
    path("delete/<str:slug>/", views.DeleteMovieView.as_view(), name="delete_movie"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),

]