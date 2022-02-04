from django.db.models import Q
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
# from cart.cart import CART_MAGIC

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
    paginate_by = 1


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class CategoryView(GenreYear, ListView):
    model = Category
    # queryset = Movie.objects.get(category_id=id)
    template_name = 'movies/category_list.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        slug = context['category_list']
        movie = slug.values('movie')
        movie = Movie.objects.filter(id=movie)
        return ({'movies': movie})


class CategoryDetailView(GenreYear, DetailView):
    model = Category
    template_name = 'movies/category_detail.html'
    slug_field = 'url'


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
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


class SearchMovieView(ListView):
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["results"] = f'q={self.request.GET.get("q")}&'
        return context

#
# @login_required()
# def cart_add(request, id):
#     cart = Cart(request)
#     movie = Movie.objects.get(id=id)
#     cart.add(product=movie)
#     return redirect("media")
#
#
# @login_required()
# def item_clear(request, id):
#     cart = Cart(request)
#     movie = Movie.objects.get(id=id)
#     cart.remove(movie)
#     return redirect("cart_detail")
#
#
# @login_required()
# def item_increment(request, id):
#     cart = Cart(request)
#     movie = Movie.objects.get(id=id)
#     cart.add(product=movie)
#     return redirect("cart_detail")
#
#
# @login_required()
# def item_decrement(request, id):
#     cart = Cart(request)
#     movie = Movie.objects.get(id=id)
#     cart.decrement(product=movie)
#     return redirect("cart_detail")
#
#
# @login_required()
# def cart_clear(request):
#     cart = Cart(request)
#     cart.clear()
#     return redirect("cart_detail")
#
#
# @login_required()
# def cart_detail(request):
#     return render(request, 'cart/cart_detail.html')