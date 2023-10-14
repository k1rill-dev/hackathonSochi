import httpx
import time
import requests

start = time.time()
url = 'http://localhost:8000/api/endpoint_video'
# files = [('files', open('/home/kirill/PycharmProjects/38.mp4', 'rb')),
#          ('files', open('/home/kirill/PycharmProjects/78.mp4', 'rb')),
#          ('files', open('/home/kirill/PycharmProjects/57.mp4', 'rb')),
#          ('files', open('/home/kirill/PycharmProjects/Как дела, Серебряков .mp4', 'rb')),
#          ('files', open('/home/kirill/PycharmProjects/e.mkv', 'rb')),
#          ]

files = {'file': open('/home/kirill/PycharmProjects/38.mp4', 'rb')}
headers = {'Filename': '38.mp4'}

print(requests.post(url=url, data={"data": "описание канала"}, headers=headers, files=files).json())

# with httpx.Client() as client:
#
#     r = client.post(url, data=data, files=files, headers=headers)
#
#
#     print(r.status_code, r.json(), sep=' ')
end = time.time()
print(f'Time elapsed: {end - start}s')
