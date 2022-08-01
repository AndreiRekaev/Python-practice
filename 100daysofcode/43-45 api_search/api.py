from typing import List
import collections
import requests


Result = collections.namedtuple('Result', 'category, id, url,'
                                          ' title, description')


def search(keyword: str) -> List[Result]:
    url = f'https://search.talkpython.fm/api/search?q={keyword}'

    resp = requests.get(url)
    resp.raise_for_status()

    search_res = resp.json()
    results = []
    for r in search_res.get('results'):
        results.append(Result(**r))

    return results
