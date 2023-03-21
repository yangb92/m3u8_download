'''
下载单个ts解密并合并
'''

import m3u8
import requests
from Crypto.Cipher import AES
import time
import os
import subprocess

output_ts = "temp.ts"
output_path = 'D:/leoyang/app/m3u8/'
# m3u8 url
url = 'https://pri-cdn-tx.xiaoeknow.com/appzBbFCNAm1880/private_index/1671761697awjDJQ.m3u8?sign=0f9c46d9f309c03ee99ad649279f0852&t=641928d5'
plist = m3u8.load(url)
key_url = plist.keys[0].absolute_uri + '&uid=u_640e935553be0_NaRrZ4fb9z'
print("[key_url] " + key_url)
response = requests.get(key_url)
if(response.status_code != 200):
    print('getKeyError')
    exit()
    
key = response.content
iv = b'0' * 16 # 偏移量
aes = AES.new(key, AES.MODE_CBC, iv)

def download_ts():
    urilist = plist.segments.uri

    # download ts list
    with open(output_ts, "wb") as f:
        for uri in urilist:
            v_url = f'https://c-vod.hw-cdn.xiaoeknow.com/2919df88vodtranscq1252524126/ee335786243791577233882899/drm/{uri}&sign=1a53e57248b633e9954f5428529c7074&t=6419d195&us=gcNfgeefXb'
            print('download: ' + v_url)
            r = requests.get(v_url, stream=True)
            f.write(aes.decrypt(r.content))
            # time.sleep(1)
            break
    
def decrypt():
    # 使用FFmpeg处理文件
    subprocess.call(['ffmpeg', '-i', output_ts, '-c:v', 'copy', '-c:a', 'copy', os.path.join(output_path, 'output_processed.mp4')])

download_ts()
decrypt()