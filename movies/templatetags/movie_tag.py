from django import template

from account.views import RegisterView
from movies.models import Category, Movie


register = template.Library()


@register.simple_tag()
def get_categories():
    category = Category.objects.all()
    print(category)
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    movies = Movie.objects.order_by("id")[:count]
    return {"last_movies": movies}

@register.simple_tag()
def get_users():
    return RegisterView.objects.all()
