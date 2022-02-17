import collections
import requests

Location = collections.namedtuple('Location', 'city state country')
Weather = collections.namedtuple('Weather', 'location units temp condition')


    # Convert plaintext over to data we can use
    loc = convert_plaintext_location(location_text)
    if not loc:
        print(f"Could not find anything about {location_text}.")
        return


    # Get report from the APi
    weather = call_weather_api(loc)
    if not weather:
        print(f"Could not get weather for {location_text} from the API.")
        return

    # Report the weather
    report_weather(loc, weather)


def report_weather(loc, weather):
    location_name = get_location_name(loc)
    scale = get_scale(weather)
    print(f'The weather in {location_name} is {weather.temp} {scale} and {weather.condition}.')


def get_scale(weather):
    if weather.units == 'imperial':
        scale = 'F'
    else:
        scale = 'C'
    return scale


def get_location_name(location):
    if not location.state:
        return f'{location.city.capitalize()}, {location.country.upper()}'
    else:
        return f'{location.city.capitalize()}, {location.state.upper()}, {location.country.upper()}'

def call_weather_api(loc):
    url = f'https://weather.talkpython.fm/api/weather?city={loc.city}&country={loc.country}&units=imperial'
    if loc.state:
        url += f'&state={loc.state}'
    # print(f"Would call {url}")
    resp = requests.get(url)
    if resp.status_code in {400, 404, 500}:
        print(f"Error: {resp.text}")
        return None

    data = resp.json()

    return convert_api_to_weather(data, loc)


def convert_api_to_weather(data, loc):
    temp = data.get('forecast').get('temp')
    w = data.get('weather')
    condition = f"{w.get('category')}: {w.get('description').capitalize()}"
    weather = Weather(loc, data.get('units'), temp, condition)
    return weather
    

def convert_plaintext_location(location_text):
    if not location_text or not location_text.strip():
        return None

    location_text = location_text.lower().strip()
    parts = location_text.split(',')

    city = ""
    state = ""
    country = 'us'
    if len(parts) == 1:
        city = parts[0].strip()
    elif len(parts) == 2:
        city = parts[0].strip()
        country = parts[1].strip()
    elif len(parts) == 3:
        city = parts[0].strip()
        state = parts[1].strip()
        country = parts[2].strip()
    else:
        return None
    # print(f"City={city}, State={state}, Country={country}")
    return Location(city, state, country)

def show_header():
    print('_________________________________________')
    print('           WEATHER CLIENT')
    print('_________________________________________')
    print()

def main():
    show_header()
    # Get the location request
    location_text = input("Where do you want the weather report (e.g. Moscow, Russia)? ")


if __name__ == '__main__':
    main()
 
