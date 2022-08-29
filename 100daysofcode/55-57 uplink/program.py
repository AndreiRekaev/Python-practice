from api import MovieSearchClient


def main():
  
  """Movie search service by keyword, director or imdb number. Enjoy!"""
  
    while True:
        print("What would you like to search next?")
        print("Enter any text for quit.")
        val = input('Search by keyword - 1, by movie director - 2 or by imdb number - 3? ')

        if val == '1':
            s_movies()
        elif val == '2':
            movie_dir()
        elif val == '3':
            imdb_mov()
        else:
            print("Good bye!")
            break


def s_movies():
    svc = MovieSearchClient()
    keyword = input('Enter keyword for search: ')
    response = svc.search_movies(keyword)
    movies = response.json()
    print()
    for idx, m in enumerate(movies.get('hits'), 1):
        print(f"{idx}. {m.get('title')} ({m.get('year')})")


def movie_dir():
    svc = MovieSearchClient()
    director = input('Enter director for movie search: ')
    response = svc.movies_by_director(director)
    movies_by_director = response.json()
    print(f"Director: {director}")
    print(movies_by_director)
    for idx, d in enumerate(movies_by_director.get('hits'), 1):
        print(f"{idx}. {d.get('title')} ({d.get('year')}) " 
              f"{d.get('genres')}")


def imdb_mov():
    svc = MovieSearchClient()
    imdb_num = input('Enter imdb number: ')
    response = svc.movies_by_imdb(imdb_num)
    try:
        movie = response.json()
        print()
        print(f"Details for movie: {movie.get('imdb_code')}")
        print(f"Title: {movie.get('title')}")
        print(f"Director: {movie.get('director')}")
        print(f"Duration: {movie.get('duration')} min")
        print(f"Genres: {movie.get('genres')}")
        print(f"Rating: {movie.get('rating')}")
        print(f"Year: {movie.get('year')}")
        print(f"IMDB score: {movie.get('imdb_score')}")
        print()
    except:
        print("Try again!")
        print()


if __name__ == '__main__':
    main()
