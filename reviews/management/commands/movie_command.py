from django.core.management.base import BaseCommand, CommandError
import requests
from reviews.models import Movies
from reviews.movies_api_integration import movies_to_db


class Command(BaseCommand):
    help = 'An integrated third party movie api to fetch and store movie data to the database'

    def handle(self, *args, **options):
        try:
            movies = movies_to_db()
            print(movies)
        except Exception as e:
            raise CommandError(e)
        
        self.stdout.write(self.style.SUCCESS("Successfully fetched movies from omdbapi and stored movie titles in the database"))

        
