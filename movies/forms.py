from django import forms
from .models import Reviews, RatingStar, Rating, Movie


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)


class CreateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class UpdateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

