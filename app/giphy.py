# Dependencies

# general
import os
from random import choice, randrange

# data
import json
from urllib import parse, request

# Funcs

def get_gif(query: str | list, limit: int = 5):
    '''
    get gif url
    '''

    # if list, pick one query randomly
    if isinstance(query, list):
        query = choice(query)

    # randomly pick one gif
    idx = randrange(limit)

    # get gif
    url = "http://api.giphy.com/v1/gifs/search"
    params = parse.urlencode({
        "q": query,
        "api_key": os.environ['GIPHY_KEY'],
        "limit": str(limit)
    })
    with request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    return data['data'][idx]['images']['downsized_medium']['url']