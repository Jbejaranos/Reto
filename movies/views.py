from django.shortcuts import render
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.

#View for the home page
def home(request):
    return render(request,"movies/home.html")

#View for the list of movies 
class IndexView(LoginRequiredMixin,generic.ListView):
    template_name = "movies/index.html"
    context_object_name = "moviesList"
    paginate_by = 10

    #Alter the get method for the generic view
    def get_queryset(self):
        user = User.objects.get(username=self.request.user)
        #Get the relationship objects
        movieUserObjects = MovieUser.objects.filter(username=user)
        #Get the movie objects to display
        movies = []
        if movieUserObjects:
            for movieUserObject in movieUserObjects:
                movies.append(movieUserObject.movie)

        return movies


#View for the details of the movies
class DetailView(generic.DetailView):
    model = Movie
    template_name = "movies/detail.html"


#View for adding a movie to an user's list
@login_required
def addMovie(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddMovieForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            #Get the data from the API
            name = form.cleaned_data['name']

            key = os.environ.get('API_KEY')

            url = f'http://www.omdbapi.com/?apikey={key}&t={name}'
            print(url)

            data = requests.get(url)
            
            data2 = data.json()

            #Use the data to get or create the movie object
            movieSearched = Movie.objects.get_or_create(
                name=name,
                year=data2["Year"],
                director=data2["Director"],
                genre=data2["Genre"],
                image = data2["Poster"])
            
            user= User.objects.get(username=request.user)

            #Create a movieUser object if it does not exist yet
            MovieUser.objects.get_or_create(movie=movieSearched[0],username=user)


            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AddMovieForm(initial={'movie': "search"})

    context = {
        'form': form,
    }

    return render(request, 'movies/addMovie.html', context)

