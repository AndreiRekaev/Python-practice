# Find your film in OMDB

import json
from pprint import pprint

import requests

# api key d4ffd1ec

def dict_by_title(apikey, title):
    url = "http://www.omdbapi.com/?t=" + title + "&apikey=" + apikey
    ret = requests.get(url)
    moviedict = json.loads(ret.text)
    return moviedict

def main():
    apikey = input('Enter your api key: ')
    title = input('Enter movie title: ')
    moviedict = dict_by_title(apikey, title)


    if moviedict["Response"] == "True":
        print("---------------------------")

        print(moviedict["Title"] + " (" + moviedict["Year"] + ")")
        pprint(moviedict["Genre"])
        pprint(moviedict["Runtime"])
        pprint("Language: " + moviedict["Language"])
        pprint("Director: " + moviedict["Director"])

        print("---------------------------")

        print(moviedict["Plot"])

        print("---------------------------")

        pprint("Actors: " + moviedict["Actors"])
    else:
        pprint("Movie not found. Try again.")


if __name__ == '__main__':
    main()
