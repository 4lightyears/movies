from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Movie, Review

from .forms import ReviewForm


def home(request):
    """landing page"""
    search_term = request.GET.get('searchMovie')

    if search_term:
        movies = Movie.objects.filter(
            title__icontains=search_term).order_by('title')
    else:
        movies = Movie.objects.all().order_by('title')

    return render(request, 'home.html', {
        'searchTerm': search_term,
        'movies': movies
    })


def detail(request, movie_id):
    """returns detail page for the selected movie"""
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)

    return render(request, 'detail.html', {
        'movie': movie,
        'reviews': reviews
    })


def about(request):
    return HttpResponse('<h1>Welcome to the about page</h1>')


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


@login_required
def create_review(request, movie_id):
    """creates a new review"""

    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        return render(request, 'create_review.html', {
            'form': ReviewForm(),
            'movie': movie
        })
    else:
        try:
            form = ReviewForm(request.POST)
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.movie = movie
            new_review.save()
            return redirect('detail', new_review.movie.id)
        except ValueError:
            return render(request, 'create_review.html', {
                'form': ReviewForm(),
                'error': 'Bad data passed in'
            })


@login_required
def update_review(request, review_id):
    """update a movie review"""

    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == 'GET':
        form = ReviewForm(instance=review)

        return render(request, 'update_review.html', {
            'review': review,
            'form': form
        })
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)

        except ValueError:
            return render(request, 'update_review.html', {
                'form': form,
                'error': 'Bad data in form'
            })


@login_required
def delete_review(request, review_id):
    """deletes a review"""

    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()

    return redirect('detail', review.movie.id)
