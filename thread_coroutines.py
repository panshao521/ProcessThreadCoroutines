#--coding:utf-8--
from gevent import monkey;
import gevent
monkey.patch_all()
from threading import Thread
import queue
import requests
import time

def crawl(url,i):
    try:
        r = requests.get(url,timeout = 3)
        print("我是第%s个【线程+协程】" %i,url,r.status_code)
    except Exception as e:
        print(e)

def task_gevent(queue,i):
    url_list = []
    while not queue.empty():
        url = queue.get()
        url_list.append(url)
        if len(url_list) == 250:
            tasks = []
            for url in url_list:
                tasks.append(gevent.spawn(crawl,url,i))
            gevent.joinall(tasks)
    return

if __name__ == '__main__':
    queue = queue.Queue()
    urls = []
    with open("d:\\urls.txt") as fp:
        for url in fp:
            urls.append(url.strip())
    print("一共%s个url" % len(urls))
    for url in urls:
        queue.put(url)

    start = time.time()
    print("**********************开始计时**********************")
    t_list = []
    for i in range(1,5):
        t = Thread(target=task_gevent, args=(queue,i)) #多进程 + 协程
        t.start()
        t_list.append(t)
        print(t)
    for p in t_list:
        p.join()
        print(p)

    end = time.time()
    print("**********************结束计时**********************")
    print("总耗时：",end - start)
