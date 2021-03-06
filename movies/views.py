from django.db.models import Q
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required


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
    paginate_by = 2


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stuff = get_object_or_404(Movie, url=self.kwargs['slug'])
        total_likes = stuff.get_total_likes()
        context["star_form"] = RatingForm()
        context['total_likes'] = total_likes
        return context


class CategoryView(GenreYear, DetailView):
    model = Category
    template_name = 'movies/category_list.html'
    paginate_by = 2
    context_object_name = 'movies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        # movie =
        # print(movie)
        context['movie_list'] = get_object_or_404(Movie, category=self.kwargs['pk'])
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     id = self.kwargs.get('pk')
    #     queryset = Movie.objects.filter(id=id)
    #     print(queryset)
    #     print(id)
    #     return queryset


class CategoryDetailView(DetailView):
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
        slug = self.object.category.id
        self.object.delete()
        return redirect('/', slug)


class SearchMovieView(ListView):
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["results"] = f'q={self.request.GET.get("q")}&'
        return context

@login_required()
def add_to_favourites(request, id):
    movie = get_object_or_404(Movie, id=id)
    if movie.favorite.filter(id=request.user.id).exists():
        movie.favorite.remove(request.user)
    else:
        movie.favorite.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required()
def favourites_list(request):
    new = Movie.objects.filter(favorite=request.user)
    return render(request, 'cart/cart_detail.html', {'new': new})

@login_required()
def like_movie(request, pk):
    movie = get_object_or_404(Movie, id=request.POST.get('movie_id'))
    if not movie.likes.filter(id=request.user.id).exists():
        movie.likes.add(request.user)
    else:
        movie.likes.remove(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



