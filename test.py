import httpx
import time
import requests
import curlify

start = time.time()
url = 'http://0.0.0.0:8000/api/endpoint_avatar'

# files = {'file': open('/home/kirill/PycharmProjects/38.mp4', 'rb')}
# headers = {'Filename': '38.mp4'}
#
# r = requests.post(url=url, data={"data": "описание канала"}, headers=headers, files=files)
# print(r.json())
data = {'style': 'anime', 'strength': 0.78}
files = {'file': open('test.jpg', 'rb')}
headers = {'Filename': 'test.jpg'}
r = requests.post(url=url, data=data, files=files, headers=headers)

# print(curlify.to_curl(r.request))
# with httpx.Client() as client:
#
#     r = client.post(url, data=data, files=files, headers=headers)
#
#
#     print(r.status_code, r.json(), sep=' ')
end = time.time()
print(f'Time elapsed: {end - start}s')
