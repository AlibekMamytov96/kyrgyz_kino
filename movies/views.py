# from django.conf import settings
# from django.db import models
# from django.db.models import Q, OuterRef, Subquery, Case, When
# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import redirect
# from django.views.generic import ListView, DetailView
# from django.views.generic.base import View
#
# from .models import Movie, Category, Actor, Genre, Rating, Reviews
# from .forms import ReviewForm, RatingForm
#
#
# class GenreYear:
#     """Жанры и года выхода фильмов"""
#
#     def get_genres(self):
#         return Genre.objects.all()
#
#     def get_years(self):
#         return Movie.objects.filter(draft=False).values("year")
#
#
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
#
#
# class MoviesView(GenreYear, ListView):
#     """Список фильмов"""
#     model = Movie
#     queryset = Movie.objects.filter(draft=False)
#     paginate_by = 1
#
#
# class MovieDetailView(GenreYear, DetailView):
#     """Полное описание фильма"""
#     model = Movie
#     queryset = Movie.objects.filter(draft=False)
#     slug_field = "url"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["star_form"] = RatingForm()
#         context["form"] = ReviewForm()
#         return context
#
#
# class AddReview(View):
#     """Отзывы"""
#
#     def post(self, request, pk):
#         form = ReviewForm(request.POST)
#         movie = Movie.objects.get(id=pk)
#         if form.is_valid():
#             form = form.save(commit=False)
#             if request.POST.get("parent", None):
#                 form.parent_id = int(request.POST.get("parent"))
#             form.movie = movie
#             form.save()
#         return redirect(movie.get_absolute_url())
#
#
# class ActorView(GenreYear, DetailView):
#     """Вывод информации о актере"""
#     model = Actor
#     template_name = 'movies/actor.html'
#     slug_field = "name"
#
#
# class FilterMoviesView(GenreYear, ListView):
#     """Фильтр фильмов"""
#     paginate_by = 5
#
#     def get_queryset(self):
#         queryset = Movie.objects.filter(
#             Q(year__in=self.request.GET.getlist("year")) |
#             Q(genres__in=self.request.GET.getlist("genre"))
#         ).distinct()
#         return queryset
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
#         context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
#         return context
#
#
# class JsonFilterMoviesView(ListView):
#     """Фильтр фильмов в json"""
#
#     def get_queryset(self):
#         queryset = Movie.objects.filter(
#             Q(year__in=self.request.GET.getlist("year")) |
#             Q(genres__in=self.request.GET.getlist("genre"))
#         ).distinct().values("title", "tagline", "url", "poster")
#         return queryset
#
#     def get(self, request, *args, **kwargs):
#         queryset = list(self.get_queryset())
#         return JsonResponse({"movies": queryset}, safe=False)
#
#
# class AddStarRating(View):
#     """Добавление рейтинга фильму"""
#
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
#
#     def post(self, request):
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             Rating.objects.update_or_create(
#                 ip=self.get_client_ip(request),
#                 movie_id=int(request.POST.get("movie")),
#                 defaults={'star_id': int(request.POST.get("star"))}
#             )
#             return HttpResponse(status=201)
#         else:
#             return HttpResponse(status=400)
#
#
# class Search(ListView):
#     """Поиск фильмов"""
#     paginate_by = 3
#
#     def get_queryset(self):
#         return Movie.objects.filter(title__icontains=self.request.GET.get("q"))
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["q"] = f'q={self.request.GET.get("q")}&'
#         return context
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .forms import ReviewForm, RatingForm, CreateMovieForm, UpdateMovieForm


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # template_name = 'movies/movies.html'


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)



class CreateMovieView(CreateView):
    model = Movie
    template_name = 'movies/create_movie.html'
    form_class = CreateMovieForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['movie_form'] = self.get_form()
        return context


class UpdateMovieView(UpdateView):
    model = Movie
    template_name = 'movies/update_movie.html'
    form_class = UpdateMovieForm
    pk_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['movie_form'] = self.get_form()
        return context


class DeleteMovieView(DeleteView):
    model = Movie
    template_name = 'movies/delete_movie.html'
    pk_url_kwarg = 'slug'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.object.category.slug
        self.object.delete()
        return redirect('/', slug)

