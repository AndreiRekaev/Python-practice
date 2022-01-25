import requests
import collections

MovieResult = collections.namedtuple('MovieResult', "imdb_code,title,duration,director,year,rating,imdb_score,keywords,genres")


def find_movies(search_text):

    if not search_text or not search_text.strip():
        raise ValueError("Search text is required")

    url = 'https://movieservice.talkpython.fm/api/search/{}'.format(search_text)

    resp = requests.get(url)
    resp.raise_for_status()

    movie_data = resp.json()
    movies_list = movie_data.get('hits')

# movies = []
# for md in movies_list:
#     m = MovieResult(
#         imdb_code=md.get('imdb_code'),
#         title=md.get('title'),
#         duration=md.get('duration'),
#         director=md.get('director'),
#         year=md.get('year'),
#         rating=md.get('rating'),
#         imdb_score=md.get('imdb_score'),
#         keywords=md.get('keywords'),
#         genres=md.get('genres')
#     )
#     movies.append(m)

# def method(x, y, z, **kwargs):
#     print("kwargs=", kwargs)
#
# method(7, 1, z=2, format=True, age=7)
    
movies = [
    MovieResult(**md)
    for md in movies_list
    ]
    movies.sort(key=lambda m: -m.year)

return movies

print("Found {} movies for search {}".format(len(movies), search))
for m in movies:
    print("{} -- {}".format(m.year, m.title))
