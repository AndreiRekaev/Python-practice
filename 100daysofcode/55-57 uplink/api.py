import uplink
import requests


@uplink.response_handler
def raise_for_status(response):
    try:
        response.raise_for_status()
    except:
        print("Something went wrong")
    return response


@uplink.json
@raise_for_status
class MovieSearchClient(uplink.Consumer):

    def __init__(self):
        super().__init__(base_url='https://movieservice.talkpython.fm/')

    @uplink.get('/api/search/{keyword}')
    def search_movies(self, keyword) -> requests.models.Response:
        """Search movies"""

    @uplink.get('/api/director/{director_name}')
    def movies_by_director(self, director_name) -> requests.models.Response:
        """Movies by director"""

    @uplink.get('/api/movie/{imdb_number}')
    def movies_by_imdb(self, imdb_number) -> requests.models.Response:
        """Movie by IMDB"""
