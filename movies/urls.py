from django.urls import path

from .import views
from .views import *

urlpatterns = [
    path('', views.MoviesView.as_view(), name='media'),
    path('create/', views.CreateMovieView.as_view(), name='create_movie'),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("update/<str:slug>/", views.UpdateMovieView.as_view(), name="update_movie"),
    path("delete/<str:slug>/", views.DeleteMovieView.as_view(), name="delete_movie"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),

    path('search', views.SearchMovieView.as_view(), name='search'),

    # cart paths
    # path('cart/add/<int:id>/', cart_add, name='cart_add'),
    # path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    # path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    # path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    # path('cart/cart_clear/', cart_clear, name='cart_clear'),
    # path('cart/cart-detail/', cart_detail, name='cart_detail'),

]