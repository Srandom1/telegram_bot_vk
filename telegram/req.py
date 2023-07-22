import requests
import Tokens
import json
def wall_get(group_name, count, offset):
    req = requests.post('https://api.vk.com/method/wall.get',
                        data={'domain': group_name, 'count': count, 'offset': offset, 'v': 5.131,
                              'access_token': Tokens.vkServiceToken})
    return json.loads(req.text)

