    w = {
"weather": {
"description": "light snow",
"category": "Snow"
},
"wind": {
"speed": 5.01,
"deg": 96
},
"units": "imperial",
"forecast": {
"temp": 31.59,
"feels_like": 26.58,
"pressure": 1013,
"humidity": 76,
"low": 27,
"high": 35
},
"location": {
"city": "Portland",
"state": "OR",
"country": "US"
},
"rate_limiting": {
"unique_lookups_remaining": 49,
"lookup_reset_window": "1 hour"
}
}
    print(w.get('forecast').get('temp'))


def main():
    d = {
        'city': 'Portland',
        'state': 'Oregon',
        'country': 'US',
        'details': ['Cold', 'Snowy', 'Winter']

    }
    print(d.get('country', 'US'))

if __name__ == '__main__':
    main()
