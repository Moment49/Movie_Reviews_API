from reviews.models import Movies
import requests

# Make the request and store the movie data[title] returned from the api to the database
def get_movies(pages):
    movies_list = []
    for page in range(1, pages+1):
        r = requests.get(f'https://www.omdbapi.com/?s=Gemini&apikey=d9884ed3&page={page}')
        response_data = r.json()
        movies_list.append(response_data)

    return movies_list


def movies_data():
    """A function to generate the first 50 movie title from the omdbapi"""
    movies_list = []
    movies = get_movies(5)
    for movie in movies:
        movie_data = movie.pop('Search')
        for movie_d in movie_data:
            for movie_key, movie_val in movie_d.items():
                if movie_key == 'Title':
                    movies_list.append(movie_val)

    return movies_list


# Add the movies to the database
def movies_to_db():
    movie_data = movies_data()
    for movie in movie_data:
        try:
            movie_title = Movies.objects.get(title=movie)
        except Movies.DoesNotExist:
            movie_title = Movies.objects.create(title=movie)
            movie_title.save()
    return movie_data



            
    