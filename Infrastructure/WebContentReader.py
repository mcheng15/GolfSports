import time
import httplib2

def GrabWebpageContent(url):
    time.sleep(1)
    http = httplib2.Http(timeout=15)
    headers, content = http.request(url)
    return content