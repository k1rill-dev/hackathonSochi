import httpx
import time

url = 'http://localhost:8000/upload'
files = {'file': open('Seishun_Buta_Yarou_wa_Yumemiru_Shoujo_no_Yume_wo_Minai_[AniLibria_TV]_[BDRip_1080p].mkv', 'rb')}
headers = {'Filename': 'Seishun_Buta_Yarou_wa_Yumemiru_Shoujo_no_Yume_wo_Minai_[AniLibria_TV]_[BDRip_1080p].mkv'}
data = {'data': 'Hello World!'}

with httpx.Client() as client:
    start = time.time()
    r = client.post(url, data=data, files=files, headers=headers)
    end = time.time()
    print(f'Time elapsed: {end - start}s')
    print(r.status_code, r.json(), sep=' ')
