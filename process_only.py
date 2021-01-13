#--coding:utf-8--
from multiprocessing import Process,Queue
import requests
import time

def crawl_process(queue,i):
    while not queue.empty():
        try:
            url = queue.get()
            r = requests.get(url,timeout = 3)
            print("我是第%s个【进程】" %i,url,r.status_code)
        except Exception as e:
            print(e)
    return


if __name__ == '__main__':
    queue = Queue()
    urls = []
    with open("d:\\urls.txt") as fp:
        for url in fp:
            urls.append(url.strip())
    print("一共%s个url" %len(urls))
    for url in urls:
        queue.put(url)

    start = time.time()
    print("**********************开始计时**********************")
    p_list = []
    for i in range(1,5):
        p = Process(target=crawl_process, args=(queue,i)) #多进程
        p_list.append(p)
        p.start()
        print(p)
    for p in p_list:
        p.join()
        print(p)
    end = time.time()
    print("**********************结束计时**********************")
    print("总耗时：",end - start)