#--coding:utf-8--
from gevent import monkey;
import gevent
monkey.patch_all()
from tornado.queues import Queue
import requests
import time

def crawl(urls,i):
    while urls:
        url = urls.pop()
        try:
            r = requests.get(url,timeout = 3)
            print("我是第%s个【协程】" %i,url,r.status_code)
        except Exception as e:
            print(e)

def crawl_gevent(queue):
    url_list = []
    tasks = []
    i = 0
    while not queue.empty():
        url = queue.get()._result
        url_list.append(url)
        if len(url_list) == 250:
            i += 1
            tasks.append(gevent.spawn(crawl,url_list,i))
            url_list = []
    gevent.joinall(tasks)

if __name__ == '__main__':
    queue = Queue()
    urls = []
    with open("d:\\urls.txt") as fp:
        for url in fp:
            urls.append(url.strip())
    print("一共%s个url" % len(urls))
    for url in urls:
        queue.put(url)

    start = time.time()
    print("**********************开始计时**********************")
    crawl_gevent(queue)
    end = time.time()
    print("**********************结束计时**********************")
    print("总耗时：",end - start)
