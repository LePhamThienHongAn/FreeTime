#Config
m3u8_main = "https://b-g-ca-3.betterstream.co:2222/v3-hls-playback/2c54fee8575bd3446d9f96cbb807b1fccc028f593a57cac00e4381fefb77fb23c5ef650be066c90f8eafee5d4a34e989312ce1d807a06643764298435d8f29e906ed6f0089c9aca23f0c0f531e0aa433207482896ce939edf60cff043777d16f9b87c5e58b018e8d2d51df03549d08c2d1d6788185d342d2e001d4525bfc9db0219de9226552ce9223907ec2a3fdc2028de8303423f9b962d8265ca7fdfe3e12df544fadf84230be2cd833fe9baf6a4ef511938d0c973141bd8d27656ac073a1/1080/index.m3u8"
maxThread = 50




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

threadCount = 0
mutex = Lock()
def download(url, segment):
    #Control thread num
    global threadCount, urls
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
    mutex.release()


#Download all files
threads = []
count = 0
for url in urls:
    threads += [Thread(target = download, args = (url, segment[count], ))]
    count += 1

count = 0
total = len(urls)
for thread in threads:
    thread.start()

    #Wait till have free thread
    while True:
        mutex.acquire()
        if threadCount < maxThread:
            break
        mutex.release()
    mutex.release()
    count += 1
    print("%d/%d" % (count, total))

import time
while threadCount != 0:
    time.sleep(1)
    pass
