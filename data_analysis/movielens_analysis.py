from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from functools import reduce
import json
import sys
import os
import pytest
import requests
import re

class Movies:
    """
    Analyzing data from movies.csv
    """
     
    __CSV_HEADERS = ('movieId','title','genres')
    __CSV_TYPES = (int, str, str)
    
    def __init__(self, path_to_file: str):
        """
        Put here any fields that you think you will need.
        """
        self.path = path_to_file
        self.titles = {}
        self.__load_data()
        
    def __load_data(self):
        self.titles = {data[0]: data[1] for data in self.__get_next_data_line()}

    def __get_next_data_line(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            next(file)  # skip first row
            while line := file.readline():
                yield self.__parse_line(line.strip())
    
    def __parse_line(cls, data_line: str) -> list:
        if data_line.find('"') != -1:
            parts = re.split(r',\"|\",', data_line)
        else:
            parts = data_line.split(',')
            
        return [cls.__CSV_TYPES[index](parts[index])
                for index in range(len(cls.__CSV_HEADERS))]
          
        
    def dist_by_release(self) -> dict[str, int]:
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        years_distribution = Counter()
        for data in self.__get_next_data_line():
            year = re.search(r'\((\d{4})\)', data[1])        
            if year:
                year = year.group(1)
            else:
                year = 'Null'
            years_distribution[year] += 1
        release_years = dict(years_distribution.most_common())
        del release_years['Null']   
        return release_years
    
    def dist_by_genres(self) -> dict[str, int]:
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres_distribution = Counter()

        for data in self.__get_next_data_line():
            genres = data[2].split('|')
            for genre in genres:
                genre = genre.strip()
                if genre:
                    genres_distribution[genre] += 1
        genres = dict(genres_distribution.most_common())
        return genres
        
    def most_genres(self, n) -> dict[str, int]:
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        dict_movies = {}
        for data in self.__get_next_data_line():
            dict_movies[data[1]] = len(data[2].split('|'))

        return dict(sorted(dict_movies.items(), key=lambda x: x[1], reverse=True)[:n])

    def get_movie_title(self, movie_id) -> str:
        """
        The method receives a list of IDs (as int) as input and returns a list of movie titles
        """
        return self.titles.get(movie_id)
    

class Tags:
    """
    Analyzing data from tags.csv
    """
    __CSV_HEADERS = ('userId','movieId','tag','timestamp')
    __CSV_TYPES = (int, int, str, int)
        
    def __init__(self, path_to_the_file: str):
        """
        Put here any fields that you think you will need.
        """
        self.path = path_to_the_file
    
    def __get_next_data_line(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            next(file)  # skip first row
            while line := file.readline():
                yield self.__parse_line(line.strip())
    
    def __parse_line(cls, data_line: str) -> list:
        parts = data_line.split(',')
            
        return [cls.__CSV_TYPES[index](parts[index])
                for index in range(len(cls.__CSV_HEADERS))]
        
        
    def most_words(self, n) -> dict[str, int]:
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = {}
        for data in self.__get_next_data_line():
            if data[2] not in big_tags:
                big_tags[data[2]] = len(re.findall(r'\w+', data[2]))
        return dict(sorted(big_tags.items(), key=lambda item: item[1], reverse=True)[:n])

    def longest(self, n) -> list[str]:
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        big_tags = {}
        for data in self.__get_next_data_line():
            if data[2] not in big_tags:
                big_tags[data[2]] = len(data[2])
        
        big_tags = dict(sorted(big_tags.items(), key=lambda item: item[1], reverse=True)[:n])
        return list(big_tags.keys())[:n]
     

    def most_words_and_longest(self, n) -> list[str]:
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        big_tags = list(self.most_words(n).keys())
        long_tags = self.longest(n)
        for value in long_tags:
            if value not in big_tags:
                big_tags.append(value)

        return big_tags
        
    def most_popular(self, n) -> dict[str, int]:
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        all_tags = []
        for data in self.__get_next_data_line():   
            all_tags.append(data[2])
        return dict(Counter(all_tags).most_common(n))
        
    def tags_with(self, word) -> list[str]:
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        tags = []
        for data in self.__get_next_data_line():
            if word.lower() in data[2].lower():
                if data[2] not in tags:
                    tags.append(data[2])
        return sorted(tags)

class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(self, path_to_the_file):
        if not os.path.isfile(path_to_the_file) or not os.access(path_to_the_file, os.R_OK):
            raise ValueError(f'file {path_to_the_file} not found or permission is denied')
        self.path_to_the_file = path_to_the_file
                    
    def __read_data__(self):
        with open(self.path_to_the_file) as file:
            file.readline()
            for _ in range(1000):
                yield file.readline()
    
    __data_reader__ = __read_data__

    class Movies:
        def __init__(self, ratings):
            self.__data_reader__ = lambda: ratings.__data_reader__()

            system_name = sys.platform
            delimer = '/'
            if system_name == 'win32' or system_name == 'cygwin' or system_name == 'msys':
                delimer = '\\'
                
            self.datadir = delimer.join(ratings.path_to_the_file.split(delimer)[:-1]) + delimer

        def __get_values__(self, row) -> list:
            values = row.split(',')
            values[0] = int(values[0])
            values[1] = int(values[1])
            values[2] = float(values[2])
            values[3] = datetime.fromtimestamp(int(values[3]), timezone.utc).year
            return values

        def __average__(self, values) -> float:
            sum = reduce(lambda x, y: x + y, values)
            average = sum / len(values)
            
            return average

        def __median__(self, values) -> float:
            median = values[len(values) // 2]

            return median
        
        def dist_by_year(self) -> dict:
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            
            years = map(lambda row: self.__get_values__(row)[3], self.__data_reader__())

            ratings_by_year = { year:count for year, count in sorted(Counter(years).items(), key=lambda item: int(item[0])) }

            return ratings_by_year
        
        def dist_by_rating(self) -> dict:
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """

            ratings = map(lambda row: self.__get_values__(row)[2], self.__data_reader__())

            ratings_distribution = {rating:count for rating, count in sorted(Counter(ratings).items(), key=lambda item: item[0])}

            return ratings_distribution
        
        def top_by_num_of_ratings(self, n) -> dict:
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """

            if n < 0:
                raise ValueError('n must be over 0')

            movies = map(lambda row: self.__get_values__(row)[1], self.__data_reader__())

            top_movies_ids = Counter(movies).most_common(n)

            top_movies = dict(top_movies_ids)

            return top_movies
        
        def top_by_ratings(self, n, metric='average') -> dict:
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """

            if n < 0:
                raise ValueError('n must be over 0')

            metrics = {
                'average': self.__average__,
                'median': self.__median__
            }
            
            if metric not in metrics:
                raise ValueError(f"Incorrect metric '{metric}'. Use 'average' or 'median'")
            
            movies_and_ratings = map(lambda row: self.__get_values__(row)[1:3], self.__data_reader__())

            movies_dict = {}
            for movie, rating in movies_and_ratings:
                if movie in movies_dict:
                    movies_dict[movie].append(rating)
                else:
                    movies_dict[movie] = [rating]

            for movie, rating in movies_dict.items():
                metric_value = metrics[metric](rating)
                movies_dict[movie] = metric_value

            if n > len(movies_dict):
                n = len(movies_dict)

            top_movies = { movie:metric_value for movie, metric_value in sorted(
                movies_dict.items(),
                key=lambda item: item[1],
                reverse=True)[:n] }
            
            return top_movies
        
        def top_controversial(self, n) -> dict:
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """

            if n < 0:
                raise ValueError('n must be over 0')

            movies_and_ratings = map(lambda row: self.__get_values__(row)[1:3], self.__data_reader__())

            movie_rating_variance = {}
            for movie, rating in movies_and_ratings:
                if movie in movie_rating_variance:
                    if rating > movie_rating_variance[movie]['top']:
                        movie_rating_variance[movie]['top'] = rating
                    elif rating < movie_rating_variance[movie]['bottom']:
                        movie_rating_variance[movie]['bottom'] = rating
                else:
                    movie_rating_variance[movie] = {'top': rating, 'bottom': rating}
            
            if n > len(movie_rating_variance):
                n = len(movie_rating_variance)

            top_movies = { movie:round(rating['top'] - rating['bottom'], 2) for movie, rating in sorted(
                movie_rating_variance.items(),
                key=lambda item: item[1]['top'] - item[1]['bottom'],
                reverse=True)[:n] }

            return top_movies
        
        def top_years_by_rating(self, n, metric='average') -> dict:
            if n < 0:
                raise ValueError('n must be over 0')
            
            metrics = {
                'average': self.__average__,
                'median': self.__median__
            }
            
            if metric not in metrics:
                raise ValueError(f"Incorrect metric '{metric}'. Use 'average' or 'median'")
            
            ratings_years = map(lambda row: self.__get_values__(row)[2:], self.__data_reader__())

            year_ratings_dict = {}
            for rating, year in ratings_years:
                if year in year_ratings_dict:
                    year_ratings_dict[year].append(rating)
                else:
                    year_ratings_dict[year] = [rating]
            
            for year, ratings in year_ratings_dict.items():
                metric_value = metrics[metric](ratings)
                year_ratings_dict[year] = metric_value

            if n > len(year_ratings_dict):
                n = len(year_ratings_dict)

            top_years = { year:round(metric_value, 2) for year, metric_value in sorted(
                year_ratings_dict.items(),
                key=lambda item: item[1],
                reverse=True
            )[:n] }

            return top_years

    class Users(Movies):
        def dist_by_rating_count(self) -> dict:
            """
            Returns the distribution of users by number of ratings made by them
            """

            users = map(lambda row: self.__get_values__(row)[0], self.__data_reader__())
            ratings_by_users = { user:ratings_count for user, ratings_count in sorted(Counter(users).most_common(),
                                                                                     key=lambda item: item[0]) }

            return ratings_by_users

        def dist_by_rating_value(self, metric='average') -> dict:
            """
            Returns the distribution of users by average or median ratings made by them
            """

            metrics = {
                'average': self.__average__,
                'median': self.__median__
            }

            if metric not in metrics:
                raise ValueError(f"Incorrect metric '{metric}'. Use 'average' or 'median'")
            
            users_and_ratings = map(
                lambda row: [ self.__get_values__(row)[0], self.__get_values__(row)[2] ],
                self.__data_reader__())
            
            users_rating_metric = {}
            for user, rating in users_and_ratings:
                if user in users_rating_metric:
                    users_rating_metric[user].append(rating)
                else:
                    users_rating_metric[user] = [rating]

            for user, rating in users_rating_metric.items():
                metric_value = metrics[metric](rating)
                users_rating_metric[user] = metric_value

            users_rating_metric = { user:round(metric_value, 2) for user, metric_value in sorted(
                users_rating_metric.items(),
                key=lambda item: item[1], reverse=True) }

            return users_rating_metric

        def top_controversial(self, n) -> dict:
            """
            Top-n users with the biggest variance of their ratings
            """

            if n < 0:
                raise ValueError('n must be over 0')
            
            users_and_ratings = map(
                lambda row: [ self.__get_values__(row)[0], self.__get_values__(row)[2] ],
                self.__data_reader__())
            
            users_rating_variance = {}
            for movie, rating in users_and_ratings:
                if movie in users_rating_variance:
                    if rating > users_rating_variance[movie]['top']:
                        users_rating_variance[movie]['top'] = rating
                    elif rating < users_rating_variance[movie]['bottom']:
                        users_rating_variance[movie]['bottom'] = rating
                else:
                    users_rating_variance[movie] = {'top': rating, 'bottom': rating}

            if n > len(users_rating_variance):
                n = len(users_rating_variance)

            top_users = { user:round(rating['top'] - rating['bottom'], 2) for user, rating in sorted(
                users_rating_variance.items(),
                key=lambda item: item[1]['top'] - item[1]['bottom'],
                reverse=True)[:n] }
            
            return top_users

class Links:
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        if not os.path.isfile(path_to_the_file) or not os.access(path_to_the_file, os.R_OK):
            raise ValueError(f'file {path_to_the_file} not found or permission is denied')
        self.path_to_the_file = path_to_the_file
    
    def __get_file_lines_offset__(self) -> list:
            with open(self.path_to_the_file) as file:
                line_offsets = []
                offset = 0

                for line in file:
                    line_offsets.append(offset)
                    offset += len(line) + 1

                file.seek(0)

            return line_offsets
    
    def __imdb_id_search__(self, id, offsets) -> str:
        max = len(offsets)
        low = 1
        high = max - 1
        
            
        with open(self.path_to_the_file) as file:
            while low <= high:
                mid = (low + high) // 2

                if mid >= max:
                    raise ValueError(f'Id {id} is out of range')

                file.seek(offsets[mid])
                row = file.readline().strip().split(',')

                if int(row[0]) < id:
                    low = mid + 1
                elif int(row[0]) > id:
                    high = mid - 1
                else:
                    return row[1]
            
        raise ValueError(f'Id {id} is out of range')
    
    def __get_director__(self, props):
        director = props['directors']
        if director is not None and len(director) > 0:
            director = director[0]['credits'][0]['name']['nameText']['text']
            return director
        else:
            return None
    
    def __get_budget__(self, props):
        budget = props['productionBudget']
        if budget is not None:
            budget = budget['budget']['amount']
            return int(budget)
        else:
            return None
        
    def __get_gross__(self, props):
        gross = props['worldwideGross']
        if gross is not None:
            gross = gross['total']['amount']
            return int(gross)
        else:
            return None
        
    def __get_runtime__(self, props):
        runtime = props['runtime']
        if runtime is not None:
            runtime = int(runtime['seconds']) // 60
            return runtime
        else:
            return None
        
    def __get_title__(self, props):
        title = props['originalTitleText']
        if title is not None:
            title = title['text']
            return title
        else:
            return None
        
    def __get_awards__(self, props):
        total_awards = props['wins']
        if total_awards is None:
            total_awards = 0
        else:
            total_awards = int(total_awards['total'])

        prestigious_awards = props['prestigiousAwardSummary']
        if prestigious_awards is not None:
            prestigious_awards = int(prestigious_awards['wins'])
            if prestigious_awards is None:
                prestigious_awards = 0
        else:
            prestigious_awards = 0

        awards = {
            'prestigious awards': prestigious_awards,
            'other awards': total_awards - prestigious_awards
        }
        
        return awards

    def __get_movie_imdb__(self, id, imdb_id, list_of_fields):
        headers = {'User-Agent': 'Mozilla/5.0 Firefox/45.0'}
        url = f'https://www.imdb.com/title/tt{imdb_id}'
        html_page = requests.get(url, headers=headers)

        soup = BeautifulSoup(html_page.content, 'html.parser').find('body')
        soup = soup.find('script', {'id':'__NEXT_DATA__', 'type':'application/json'}).get_text()

        props = json.loads(soup)['props']['pageProps']['mainColumnData']
        
        movie_inf = {
            'director': self.__get_director__(props),
            'budget': self.__get_budget__(props),
            'cumulative worldwide gross': self.__get_gross__(props),
            'runtime': self.__get_runtime__(props),
            'title': props['originalTitleText']['text'],
            'awards': self.__get_awards__(props)
        }

        for field in list_of_fields:
            if field not in movie_inf:
                raise ValueError('No such field for movies.')

        movie_out = [ id ] + [ movie_inf[field.lower()] for field in list_of_fields ]
    
        return movie_out
    
    def __get_first_ids__(self, n=10):
        with open(self.path_to_the_file) as file:
            file.readline()
            for _ in range(n):
                yield int(file.readline().split(',')[0])

    
    def get_imdb(self, list_of_movies, list_of_fields) -> list:
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """

        file_offsets = self.__get_file_lines_offset__()
        movie_id_imdb_id = [ [int(id), self.__imdb_id_search__(int(id), file_offsets)] for id in list_of_movies ]

        imdb_info = sorted([ self.__get_movie_imdb__(*movie_ids, list_of_fields) for movie_ids in movie_id_imdb_id ],
                           key=lambda movie: movie[0],
                           reverse=True)

        return imdb_info
        
    def top_directors(self, n) -> dict:
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """

        if n < 0:
            raise ValueError('n must be over 0')
        
        reader = lambda: self.__get_first_ids__()
        directors = filter(
            lambda item: item[0] is not None,
            [ director for _, director in self.get_imdb(reader(), ['director']) ])
        
        directors = dict(Counter(directors).most_common(n))

        return directors
        
    def most_expensive(self, n) -> dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """

        if n < 0:
            raise ValueError('n must be over 0')

        reader = lambda: self.__get_first_ids__()
        budgets = filter(
            lambda item: item[0] is not None and item[1] is not None,
            [ [ title, budget ] for _, title, budget in self.get_imdb(reader(), ['title', 'budget']) ])

        budgets = sorted(budgets,
                         key=lambda item: item[1],
                         reverse=True)
        
        if n > len(budgets):
            n = len(budgets)

        budgets = { title:budget for title, budget in budgets[:n] }

        return budgets
        
    def most_profitable(self, n) -> dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """

        if n < 0:
            raise ValueError('n must be over 0')

        reader = lambda: self.__get_first_ids__()
        profits = filter(
            lambda item: item[0] is not None and item[1] is not None and item[2] is not None,
            [ [title, budget, gross] for _, title, budget, gross in self.get_imdb(reader(), ['title', 'budget', 'cumulative worldwide gross']) ]
        )

        profits = sorted(profits,
                         key=lambda item: item[2] - item[1],
                         reverse=True)
        
        if n > len(profits):
            n = len(profits)

        profits = { title:gross - budget for title, budget, gross in profits[:n] }

        return profits
        
    def longest(self, n) -> dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version - choose any.
        Sort it by runtime descendingly.
        """

        if n < 0:
            raise ValueError('n must be over 0')

        reader = lambda: self.__get_first_ids__()
        runtimes = filter(
            lambda item: item[0] is not None and item[1] is not None,
            [ [title, runtime] for _, title, runtime in self.get_imdb(reader(), ['title', 'runtime']) ]
        )

        runtimes = sorted(runtimes,
                          key=lambda item: item[1],
                          reverse=True)
        
        if n > len(runtimes):
            n = len(runtimes)

        runtimes = { title:runtime for title, runtime in runtimes[:n] }

        return runtimes
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies - do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """

        if n < 0:
            raise ValueError('n must be over 0')

        reader = lambda: self.__get_first_ids__()
        costs = filter(
            lambda item: item[0] is not None and item[1] is not None and item[2] is not None,
            [ [title, runtime, budget] for _, title, runtime, budget in self.get_imdb(reader(), ['title', 'runtime', 'budget']) ]
        )
        
        costs = sorted(costs,
                       key=lambda item: item[2] / item[1],
                       reverse=True)
        
        if n > len(costs):
            n = len(costs)

        costs = { title:round(gross / runtime, 2) for title, runtime, gross in costs[:n]}

        return costs
    
    def top_awarded(self, n) -> dict:
        if n < 0:
            raise ValueError('n must be over 0')
        
        reader = lambda: self.__get_first_ids__()

        awards = filter(
            lambda item: item[0] is not None,
            [ [title, award] for _, title, award in self.get_imdb(reader(), ['title', 'awards']) ]
        )

        awards = sorted(awards,
                       key=lambda item: (item[1]['prestigious awards'],
                                         item[1]['other awards']),
                       reverse=True)
        
        if n > len(awards):
            n = len(awards)
        
        awards = { title:award for title, award in awards[:n] }

        return awards

class Tests:
    """Tests class
    """
    class TestMovies:
        """Tests for Movies class
        """

        def setup_class(cls):
            cls.mov = Movies('./ml-latest-small/movies.csv')

        def test__dist_by_release_sorted(self):
            result = self.mov.dist_by_release()
            releases = list(result.values())
            sorted = True
            for i in range(1, len(releases)):
                if releases[i - 1] < releases[i]:
                    sorted = False
                    break
            assert sorted

        def test__dist_by_release_type(self):
            result = self.mov.dist_by_release()
            assert isinstance(result, dict)

        def test__dist_by_genres_sorted(self):
            result = self.mov.dist_by_genres()
            genres = list(result.values())
            sorted = True
            for i in range(1, len(genres)):
                if genres[i - 1] < genres[i]:
                    sorted = False
                    break
            assert sorted

        def test__dist_by_genres_type(self):
            result = self.mov.dist_by_genres()
            assert isinstance(result, dict)

        def test__most_genres_sorted(self):
            result = self.mov.most_genres(10)
            genres = list(result.values())
            sorted = True
            for i in range(1, len(genres)):
                if genres[i - 1] < genres[i]:
                    sorted = False
                    break
            assert sorted

        def test__most_genres_type(self):
            result = self.mov.most_genres(10)
            assert isinstance(result, dict)

        def test_get_movie_title_type(self):
            result = self.mov.get_movie_title(8)
            assert isinstance(result, str)

        def test_get_movie_title_check_result(self):
            assert self.mov.get_movie_title(5) == 'Father of the Bride Part II (1995)'

        def test_get_movie_title_incorrect_id(self):
            assert self.mov.get_movie_title(98222222222222222222222222523) is None
    
    class TestTags:
        """Tests for Tags class
        """
        def setup_class(cls):
            cls.tags = Tags('./ml-latest-small/tags.csv')

        def test__most_words__types(self):
            result = self.tags.most_words(10)
            assert isinstance(result, dict)

        def test__most_words__is_sorted(self):
            result = self.tags.most_words(10)

            sorted_list = True
            words = list(result.values())
            for i in range(1, len(words)):
                if words[i - 1] < words[i]:
                    sorted_list = False
                    break
            assert sorted_list
            
            # check len
            assert len(result) == 10

        def test__longest__types(self):
            result = self.tags.longest(10)
            assert isinstance(result, list)

        def test__longest__is_sorted(self):
            result = self.tags.longest(10)
            sorted_list = True
            for i in range(1, len(result)):
                if len(result[i - 1]) < len(result[i]):
                    sorted_list = False
                    break
            assert sorted_list
    
            # check len
            assert len(result) == 10

        def test_most_words_and_longest_types(self):
            result = self.tags.most_words_and_longest(10)
            assert isinstance(result, list)

        def test_most_words_and_longest_duplicates(self):
            my_list = self.tags.most_words_and_longest(10)
            test_set = set(my_list)
            assert len(my_list) == len(test_set)

        def test_most_popular_type(self):
            result = self.tags.most_popular(10)
            assert isinstance(result, dict)

        def test_most_popular_duplicates(self):
            my_list = list(self.tags.most_popular(10).keys())
            test_set = set(my_list)
            assert len(my_list) == len(test_set)

        def test_most_popular_sorted(self):
            result = self.tags.most_popular(10)
            
            tag = list(result.values())
            sorted_list = True
            for i in range(1, len(tag)):
                if tag[i - 1] < tag[i]:
                    sorted = False
                    break
            assert sorted_list
            
            # check len
            assert len(result) == 10

        def test_tags_with_out(self):
            word = 'comedy'
            result = self.tags.tags_with(word)
            check_word = True
            for i in range(len(result)):
                if word not in result[i].lower():
                    check_word = False
                    break
            assert check_word

        def test_tags_with_type(self):
            result = self.tags.tags_with('comedy')
            assert isinstance(result, list)

        def test_tags_with_dupl(self):
            my_list = list(self.tags.tags_with('comedy'))
            test_set = set(my_list)
            assert len(my_list) == len(test_set)

        def test_tags_with_sorted(self):
            result = self.tags.tags_with('comedy')
            sort_list = True
            for i in range(1, len(result)):
                if result[i - 1][0] > result[i][0]:
                    sort_list = False
            assert sort_list

    class TestRatings:
        def test_uncorrect_filename(self):
            with pytest.raises(ValueError):
                Ratings('not-a-file')

        @pytest.fixture
        def filename(self):
            return 'ml-latest-small/ratings.csv'
            
        @pytest.fixture
        def ratings(self, filename):
            return Ratings(filename)

        def test_attribute(self, ratings, filename):
            assert ratings.path_to_the_file == filename
            assert hasattr(ratings, '__data_reader__')

        @pytest.fixture
        def movies(self, ratings):
            return Ratings.Movies(ratings)

        def test_movies_attribute(self, movies):
            assert hasattr(movies, '__data_reader__')
            assert movies.datadir == 'ml-latest-small/'

        def test_fields_types(self, movies):
            assert type(movies.__get_values__(next(movies.__data_reader__()))[0]) is int
            assert type(movies.__get_values__(next(movies.__data_reader__()))[1]) is int
            assert type(movies.__get_values__(next(movies.__data_reader__()))[2]) is float
            assert type(movies.__get_values__(next(movies.__data_reader__()))[3]) is int

        @pytest.fixture
        def movies_dist_by_year(self, movies):
            return movies.dist_by_year()
        
        def test_movies_dist_by_year_return_type(self, movies_dist_by_year):
            assert type(movies_dist_by_year) is dict

        def test_movies_dist_by_year_sort(self, movies_dist_by_year):
            years = [ movies_dist_by_year.keys() ]
            assert all(years[i] <= years[i + 1] for i in range(len(years) - 1))

        def test_movies_dist_by_year_precalc_values(self, movies_dist_by_year):
            years = movies_dist_by_year
            precalc = {
                1996: 358,
                1999: 82,
                2000: 296,
                2001: 70,
                2005: 121,
                2006: 4,
                2007: 1,
                2011: 39,
                2015: 29
            }

            assert years == precalc

        @pytest.fixture
        def movies_dist_by_rating(self, movies):
            return movies.dist_by_rating()

        def test_movies_dist_by_rating_return_type(self, movies_dist_by_rating):
            assert type(movies_dist_by_rating) is dict

        def test_movies_dist_by_rating_sort(self, movies_dist_by_rating):
            ratings = [ movies_dist_by_rating.keys() ]
            assert all(ratings[i] <= ratings[i + 1] for i in range(len(ratings) - 1))

        def test_movies_dist_by_rating_precalc(self, movies_dist_by_rating):
            ratings = movies_dist_by_rating
            precalc = {
                0.5: 24,
                1.0: 39,
                1.5: 11,
                2.0: 57,
                2.5: 7,
                3.0: 253,
                3.5: 17,
                4.0: 292,
                4.5: 33,
                5.0: 267
            }

            assert ratings == precalc

        @pytest.fixture
        def movies_top_by_num_of_ratings(self, movies):
            return movies.top_by_num_of_ratings(5)

        def test_movies_top_by_num_of_ratings_return_type(self, movies_top_by_num_of_ratings):
            assert type(movies_top_by_num_of_ratings) is dict

        def test_movies_top_by_num_of_ratings_uncorrect_n(self, movies):
            with pytest.raises(ValueError):
                movies.top_by_num_of_ratings(-1)

        def test_movies_top_by_num_of_ratings_sort(self, movies_top_by_num_of_ratings):
            numbers = [ movies_top_by_num_of_ratings.values() ]
            assert all(numbers[i] >= numbers[i + 1] for i in range(len(numbers) - 1))

        def test_movies_top_by_num_of_ratings_precalc(self, movies_top_by_num_of_ratings):
            numbers = movies_top_by_num_of_ratings
            precalc = {
                50: 4,
                296: 4,
                457: 4,
                527: 4,
                592: 4
            }

            assert numbers == precalc

        @pytest.fixture
        def movies_top_by_ratings(self, movies):
            return movies.top_by_ratings(5)

        def test_movies_top_by_ratings_return_type(self, movies_top_by_ratings):
            assert type(movies_top_by_ratings) is dict

        def test_movies_top_by_ratings_uncorrect_n(self, movies):
            with pytest.raises(ValueError):
                movies.top_by_ratings(-1)
        
        def test_movies_top_by_ratings_uncorrect_metric(self, movies):
            with pytest.raises(ValueError):
                movies.top_by_ratings(5, metric='Kak po kaifu poschitai')

        def test_movies_top_by_ratings_sort(self, movies_top_by_ratings):
            metric_values = [ movies_top_by_ratings.values() ]
            assert all(metric_values[i] >= metric_values[i + 1] for i in range(len(metric_values) - 1))

        def test_movies_top_by_ratings_precalc(self, movies_top_by_ratings):
            metric_values = movies_top_by_ratings
            precalc = {
                101:5.00,
                157:5.00,
                260:5.00,
                661:5.00,
                919:5.00
            }

            assert metric_values == precalc

        @pytest.fixture
        def movies_top_controversial(self, movies):
            return movies.top_controversial(5)
        
        def test_movies_top_controversial_return_type(self, movies_top_controversial):
            assert type(movies_top_controversial) is dict

        def test_movies_top_controversial_uncorrect_n(self, movies):
            with pytest.raises(ValueError):
                movies.top_controversial(-1)

        def test_movies_top_controversial_sort(self, movies_top_controversial):
            variances = [ movies_top_controversial.values() ]
            assert all(variances[i] >= variances[i + 1] for i in range(len(variances) - 1))

        def test_movies_top_controversial_precalc(self, movies_top_controversial):
            variances = movies_top_controversial
            precalc = {
                527: 4.50,
                2018: 4.50,
                2090: 4.50,
                914: 4.50,
                50: 4.00
            }

            assert variances == precalc

        @pytest.fixture
        def movies_top_years_by_rating(self, movies):
            return movies.top_years_by_rating(5)
        
        def test_movies_top_years_by_rating_return_value(self, movies_top_years_by_rating):
            assert type(movies_top_years_by_rating) is dict

        def test_movies_top_years_by_rating_uncorrect_n(self, movies):
            with pytest.raises(ValueError):
                movies.top_years_by_rating(-1)

        def test_movies_top_years_by_rating_uncorrect_metric(self, movies):
            with pytest.raises(ValueError):
                movies.top_years_by_rating(5, metric='Kakoi metric, davai footik')
        
        def test_movies_top_years_by_rating_sort(self, movies_top_years_by_rating):
            years = [ movies_top_years_by_rating.values() ]
            assert all(years[i] >= years[i + 1] for i in range(len(years) - 1))

        def test_movies_top_years_by_rating_precalc(self, movies_top_years_by_rating):
            years = movies_top_years_by_rating
            precalc = {
                2000: 4.23,
                2015: 3.95,
                1999: 3.7,
                1996: 3.51,
                2005: 3.41
            }

            assert years == precalc

        @pytest.fixture
        def users(self, ratings):
            return Ratings.Users(ratings)
        
        @pytest.fixture
        def users_dist_by_rating_count(self, users):
            return users.dist_by_rating_count()
            
        def test_users_dist_by_rating_count_return_value(self, users_dist_by_rating_count):
            assert type(users_dist_by_rating_count) is dict

        def test_users_dist_by_rating_count_sort(self, users_dist_by_rating_count):
            users_rating = [ users_dist_by_rating_count.keys() ]
            assert all(users_rating[i] <= users_rating[i + 1] for i in range(len(users_rating) - 1))

        def test_users_dist_by_rating_count_precalc(self, users_dist_by_rating_count):
            users_rating = users_dist_by_rating_count
            precalc = {
                1: 232,
                2: 29,
                3: 39,
                4: 216,
                5: 44,
                6: 314,
                7: 126
            }

            assert users_rating == precalc

        @pytest.fixture
        def users_dist_by_rating_value(self, users):
            return users.dist_by_rating_value()
        
        def test_users_dist_by_rating_value_return_value(self, users_dist_by_rating_value):
            assert type(users_dist_by_rating_value) is dict

        def test_users_dist_by_rating_value_uncorrect_n(self, users):
            with pytest.raises(ValueError):
                users.dist_by_rating_value(metric='Kak po kaifu poschitai')

        def test_users_dist_by_rating_value_sort(self, users_dist_by_rating_value):
            metric_values = [ users_dist_by_rating_value.values() ]
            assert all(metric_values[i] >= metric_values[i + 1] for i in range(len(metric_values) - 1))

        def test_users_dist_by_rating_precalc(self, users_dist_by_rating_value):
            metric_values = users_dist_by_rating_value
            precalc = {
                1: 4.37,
                2: 3.95,
                5: 3.64,
                4: 3.56,
                6: 3.49,
                7: 3.35,
                3: 2.44
            }

            assert metric_values == precalc

        @pytest.fixture
        def users_top_controversial(self, users):
            return users.top_controversial(5)
        
        def test_users_top_controversial_return_value(self, users_top_controversial):
            assert type(users_top_controversial) is dict

        def test_users_top_controversial_uncorrect_n(self, users):
            with pytest.raises(ValueError):
                users.top_controversial(-1)

        def test_users_top_controversial_sort(self, users_top_controversial):
            variances = [ users_top_controversial.values() ]
            assert all(variances[i] >= variances[i + 1] for i in range(len(variances) - 1))

        def test_users_top_controversial_precalc(self, users_top_controversial):
            variances = users_top_controversial
            precalc = {
                3: 4.50,
                7: 4.50,
                1: 4.00,
                4: 4.00,
                5: 4.00
            }

            assert variances == precalc

    class TestLinks:
        def test_uncorrect_filename(self):
            with pytest.raises(ValueError):
                Links('Sam naidi')
        
        @pytest.fixture
        def links(self):
            return Links('ml-latest-small/links.csv')
        
        def test_get_imdb_return_value(self, links):
            imdb_info = links.get_imdb([1, 4, 7], ['director', 'budget', 'cumulative worldwide gross', 'runtime'])
            assert type(imdb_info) is list
            assert type(imdb_info[0]) is list

        def test_get_imdb_uncorrect_field(self, links):
            with pytest.raises(ValueError):
                links.get_imdb([1, 4, 7], ['Nu shob pacani ne zasmeiali'])

        def test_get_imdb_out_of_index(self, links):
            with pytest.raises(ValueError):
                links.get_imdb([1, 4, 1000000000000], ['director'])

        def test_get_imdb_sort(self, links):
            imdb_info = links.get_imdb([1, 5, 7, 9, 6, 3, 10], ['director', 'budget', 'runtime'])
            assert all(imdb_info[i][0] >= imdb_info[i + 1][0] for i in range(len(imdb_info) - 1))

        def test_get_imdb_precalc(self, links):
            imdb_info = links.get_imdb([1, 4, 7], ['director', 'budget', 'cumulative worldwide gross', 'runtime'])
            precalc = [
                [7, 'Sydney Pollack', 58000000, 53696959, 127],
                [4, 'Forest Whitaker', 16000000, 81452156, 124],
                [1, 'John Lasseter', 30000000, 394436586, 81]
            ]

            assert imdb_info == precalc

        @pytest.fixture
        def links_top_directors(self, links):
            return links.top_directors(5)

        def test_top_directors_return_value(self, links_top_directors):
            assert type(links_top_directors) is dict
        
        def test_top_directors_uncorrect_n(self, links):
            with pytest.raises(ValueError):
                links.top_directors(-1)
        
        def test_top_directors_sort(self, links_top_directors):
            directors = [ links_top_directors.values() ]
            assert all(directors[i] >= directors[i + 1] for i in range(len(directors) -1))

        def test_top_directors_precalc(self, links_top_directors):
            directors = links_top_directors
            precalc = {
                'Martin Campbell': 1,
                'Peter Hyams': 1,
                'Peter Hewitt': 1,
                'Sydney Pollack': 1,
                'Michael Mann': 1
            }

            assert directors == precalc
        
        @pytest.fixture
        def links_most_expensive(self, links):
            return links.most_expensive(5)
        
        def test_most_expensive_return_value(self, links_most_expensive):
            assert type(links_most_expensive) is dict

        def test_most_expensive_uncorrect_n(self, links):
            with pytest.raises(ValueError):
                links.most_expensive(-1)
        
        def test_most_expensive_sort(self, links_most_expensive):
            budgets = [ links_most_expensive.values() ]
            assert all(budgets[i] >= budgets[i + 1] for i in range(len(budgets) - 1))

        def test_most_expensive_precalc(self, links_most_expensive):
            budgets = links_most_expensive
            precalc = {
                'Jumanji': 65000000,
                'GoldenEye': 60000000,
                'Heat': 60000000,
                'Sabrina': 58000000,
                'Sudden Death': 35000000
            }

            assert budgets == precalc

        @pytest.fixture
        def links_most_profitable(self, links):
            return links.most_profitable(5)

        def test_most_profitable_return_value(self, links_most_profitable):
            assert type(links_most_profitable) is dict

        def test_most_profitable_uncorrect_n(self, links):
            with pytest.raises(ValueError):
                links.most_profitable(-1)

        def test_most_profitable_sort(self, links_most_profitable):
            profits = [ links_most_profitable.values() ]
            assert all(profits[i] >= profits[i + 1] for i in range(len(profits) - 1))

        def test_most_profitable_precalc(self, links_most_profitable):
            profits = links_most_profitable
            precalc = {
                'Toy Story': 364436586,
                'GoldenEye': 292194034,
                'Jumanji': 197821940,
                'Heat': 127436818,
                'Waiting to Exhale': 65452156
            }

            assert profits == precalc

        @pytest.fixture
        def links_longest(self, links):
            return links.longest(5)

        def test_longest_return_value(self, links_longest):
            assert type(links_longest) is dict

        def test_longest_uncorrect_n(self, links):
            with pytest.raises(ValueError):
                links.longest(-1)
        
        def test_longest_sort(self, links_longest):
            runtimes = [ links_longest.values() ]
            assert all(runtimes[i] >= runtimes[i + 1] for i in range(len(runtimes) - 1))

        def test_longest_precalc(self, links_longest):
            runtimes = links_longest
            precalc = {
                'Heat': 170,
                'GoldenEye': 130,
                'Sabrina': 127,
                'Waiting to Exhale': 124,
                'Sudden Death': 111,
            }

            assert runtimes == precalc

        @pytest.fixture
        def links_top_cost_per_minute(self, links):
            return links.top_cost_per_minute(5)

        def test_cost_per_minute_return_value(self, links_top_cost_per_minute):
            assert type(links_top_cost_per_minute) is dict

        def test_cost_per_minute_uncorrect_n(self, links):
            with pytest.raises(ValueError):
                links.top_cost_per_minute(-1)
        
        def test_cost_per_minute_sort(self, links_top_cost_per_minute):
            costs = [ links_top_cost_per_minute.values() ]
            assert all(costs[i] >= costs[i + 1] for i in range(len(costs) - 1))

        def test_cost_per_minute_precalc(self, links_top_cost_per_minute):
            costs = links_top_cost_per_minute
            precalc = {
                'Jumanji': 625000.0,
                'GoldenEye': 461538.46,
                'Sabrina': 456692.91,
                'Toy Story': 370370.37,
                'Heat': 352941.18
            }

            assert costs == precalc

        @pytest.fixture
        def links_top_awarded(self, links):
            return links.top_awarded(5)

        def test_top_awarded_return_type(self, links_top_awarded):
            assert type(links_top_awarded) is dict

        def test_top_awarded_uncorrect_n(self, links):
            with pytest.raises(ValueError):
                links.top_awarded(-1)

        def test_top_awarded_sort(self, links_top_awarded):
            awards = links_top_awarded
            prestigious_awards = [ award['prestigious awards'] for award in awards.values() ]
            assert all(prestigious_awards[i] >= prestigious_awards[i + 1] for i in range(len(prestigious_awards) - 1))

        def test_top_awarded_precalc(self, links_top_awarded):
            awards = links_top_awarded
            precalc = {
                'Toy Story': {'prestigious awards': 0, 'other awards': 29},
                'Waiting to Exhale': {'prestigious awards': 0, 'other awards': 9},
                'Jumanji': {'prestigious awards': 0, 'other awards': 4},
                'GoldenEye': {'prestigious awards': 0, 'other awards': 2},
                'Sabrina': {'prestigious awards': 0, 'other awards': 2}
            }

            assert awards == precalc
