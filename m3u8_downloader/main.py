#Config
m3u8_main = "https://b-g-eu-8.betterstream.co:2222/v3-hls-playback/2c54fee8575bd3446d9f96cbb807b1fccc028f593a57cac00e4381fefb77fb23c5ef650be066c90f8eafee5d4a34e989312ce1d807a06643764298435d8f29e9588750f13dee1175b080688427a5e40bca0600e7fe0dc4338dc63e84d3cbaa6db39a318dd7d19c2f16d77ffc5ba9d10f4ed20d4e912a82246ed31cb0408d536a963717a18313ef1cb14567e272b77fe04e1f215b449c20e6a6f185bddb4dace01eeb2927d0a037e94a180ca84abf67559480253e73a25abf418d46e484e48800/1080/index.m3u8"
maxThread = 50
skip = 0

base_url = m3u8_main[:-m3u8_main[::-1].find("/")]

import requests
#Get all segment in m3u8 file
r = requests.get(m3u8_main, verify=False)
data = r.text.replace("\r\n", "\n").split("\n")
urls = []
segment = []
for line in data:
    if (len(line) != 0):
        if (line[0] != "#"):
            urls += [base_url + line]
            segment += [line]

from threading import Thread, Lock

total = len(urls)
segment_count = 0
threadCount = 0
mutex = Lock()
def download(url, segment):
    #Control thread num
    global threadCount, urls, segment_count
    mutex.acquire()
    threadCount += 1
    mutex.release()

    r = requests.get(url, verify=False)
    while r.status_code != 200:
        r = requests.get(url, verify=False)

    while True:
        mutex.acquire()
        if urls[0] == url:
            break
        mutex.release()

    fo = open("final.ts", "ab")
    fo.write(r.content)
    fo.close()

    urls.pop(0)
    mutex.release()

    mutex.acquire()
    threadCount -= 1
    segment_count += 1
    print("%s/%s" % (segment_count,total))
    mutex.release()


#Download all files
threads = []
count = 0
for url in urls:
    if count >= skip:
        threads += [Thread(target = download, args = (url, segment[count], ))]
    count += 1

for thread in threads:
    thread.start()

    #Wait till have free thread
    while True:
        mutex.acquire()
        if threadCount < maxThread:
            break
        mutex.release()
    mutex.release()

import time
while threadCount != 0:
    time.sleep(1)
    pass
