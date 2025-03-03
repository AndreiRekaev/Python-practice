import requests
from datetime import datetime

ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'
API_VERSION = '5.81'

def get_user_id(username):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'v': API_VERSION,
        'access_token': ACCESS_TOKEN,
        'user_ids': username
    }
    response = requests.get(url, params=params).json()
    if 'response' in response:
        return response['response'][0]['id']
    else:
        raise Exception("User not found or access denied")

def get_friends(user_id):
    url = 'https://api.vk.com/method/friends.get'
    params = {
        'v': API_VERSION,
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'fields': 'bdate'
    }
    response = requests.get(url, params=params).json()
    if 'response' in response:
        return response['response']['items']
    else:
        raise Exception("Failed to fetch friends")


def calc_age(username):
    user_id = get_user_id(username)
    friends = get_friends(user_id)
    age_count = {}

    current_year = datetime.now().year

    for friend in friends:
        if 'bdate' in friend:
            bdate = friend['bdate'].split('.')
            if len(bdate) == 3:
                birth_year = int(bdate[2])
                age = current_year - birth_year
                if age in age_count:
                    age_count[age] += 1
                else:
                    age_count[age] = 1

    sorted_age_count = sorted(age_count.items(), key=lambda x: (-x[1], x[0]))
    return sorted_age_count


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)

# Stepik solution
# from json.decoder import JSONDecodeError
# from datetime import datetime
# import requests
# 
# ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da' \
#                '72454d235c274f1a2be5f45ee711'
# API_URL = 'https://api.vk.com/method'
# V = '5.71'
# 
# 
# def get_user_id(uid):
#     users_get = '{}/users.get'.format(API_URL)
#     resp = requests.get(users_get, params={
#         'access_token': ACCESS_TOKEN,
#         'user_ids': uid,
#         'v': V
#     })
#     try:
#         resp = resp.json()
#         resp = resp['response']
#         user = resp[0]
#         return user['id']
#     except (JSONDecodeError, IndexError, KeyError):
#         pass
# 
# 
# def get_friends(user_id):
#     friends_get = '{}/friends.get'.format(API_URL)
#     resp = requests.get(friends_get, params={
#         'access_token': ACCESS_TOKEN,
#         'user_id': user_id,
#         'fields': 'bdate',
#         'v': V
#     })
#     try:
#         resp = resp.json()
#         resp = resp['response']
#         return resp['items']
#     except (JSONDecodeError, KeyError):
#         pass
# 
# 
# def calc_age(uid):
#     user_id = get_user_id(uid)
#     if user_id is None:
#         return
# 
#     friends = get_friends(user_id)
#     if friends is None:
#         return
# 
#     years = {}
#     cur_year = datetime.now().year
# 
#     for friend in friends:
#         bdate = friend.get('bdate')
#         if not bdate:
#             continue
# 
#         bdate = bdate.split('.')
#         if len(bdate) != 3:
#             continue
# 
#         year = int(bdate[2])
#         diff = cur_year - year
#         years.setdefault(diff, 0)
#         years[diff] += 1
# 
#     return sorted(years.items(), key=lambda v: (v[1], -v[0]), reverse=True)
