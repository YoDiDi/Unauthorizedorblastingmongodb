# -*- coding:utf-8 -*-
# author:f0ngf0ng
from lxml import etree
import re
import threading
import time
import requests
from queue import Queue
import pymongo

'''
探测是否有未授权
'''

event = threading.Event()
event.set()
q = Queue(0)
s = time.strftime('%Y-%m-%d',time.localtime(time.time()))
exitFlag = 0

class f0ng():
    def __init__(self,url,num):
        self.url = url
        self.num = num

    def fff(self):
        url = self.url
        url = url.strip()

        try:
            client = pymongo.MongoClient("mongodb://" + url, 27017)
            mydb = client['local']
            sevenday = mydb['startup_log']
            doc = sevenday.find()
            for d in doc:
                if d:
                    print(d)
                    with open("6111.txt", "a+") as f:
                        f.writelines(url + '\n')
                    break
                else:
                    print("wrong")

        except pymongo.errors.OperationFailure:
            print("ooo")

        except pymongo.errors.ServerSelectionTimeoutError:
            print("oo")

        except pymongo.errors.ConfigurationError:
            print("o")

        except pymongo.errors.NetworkTimeout:
            print("o")

class myThread (threading.Thread):
    def __init__(self, q, num):
        threading.Thread.__init__(self)
        self.q = q
        self.num = num
        print(num)

    def run(self):
        while event.is_set():
            if self.q.empty():
                break
            else:
                sql_spot = f0ng(self.q.get(),self.num)
                sql_spot.fff()

def scan_thread(q):
    thread_num = 15
    threads = []
    for num in range(1,thread_num+1):
        t = myThread(q,num)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()



def open_urls():                                                                             #
    url_path = r'success'+ s.replace('-', '') +'.txt'
    f = open(url_path, 'r',encoding='utf-8')
    for each_line in f:

        each_line = re.sub('http://|:27017','',each_line)   #针对27017端口上的mongodb

        print(each_line)
        q.put(each_line)
    return q


if __name__ == '__main__':
    open_urls()
    scan_thread(q)