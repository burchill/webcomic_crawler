'''
Created on Oct 31, 2016

@author: zburchill
'''

from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
from PIL import Image
import io
import pickle

# for threading
import threading
from queue import Queue
import time


def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    

'''
TO-DO: use `multiprocessing` instead of `threading`.  Threading shares the same memory :(
    
    

'''

date_format = "%B %d, %Y"

# lock to serialize console output
csv_string="Date,Width,Height"
csv_string_lock = threading.Lock()


def get_image_dim(image_url_t):
    image_file = io.BytesIO(urllib.request.urlopen(urllib.parse.quote(image_url_t,safe=":/")).read())
    image_file.seek(0)
    im = Image.open(image_file)
    width, height = im.size
    return(width, height)
    
def get_and_write_image_dim(date_s,image_url_t):
    global csv_string
    try: 
        width, height = get_image_dim(image_url_t)
    except Exception as errorm:
        print(str(errorm))
        width="NA"
        height="NA"
        print("cant get dimensions for: "+image_url_t)
    csv_line="\n"+date_s+","+str(width)+","+str(height)
    with csv_string_lock:
        csv_string+=csv_line

def get_soup_stuff(soup_t, time_args, image_args, date_format="%B %d, %Y"):
    date = datetime.strptime(list(soup_t.find(*time_args).strings)[0], date_format)
    date_s = date.strftime("%x")
    image_url = soup_t.find(*image_args)['src']
    get_and_write_image_dim(date_s,image_url)
    

# The worker thread pulls an item from the queue and processes it
def worker(time_args, image_args, date_format="%B %d, %Y"):
    while True:
        item = q.get()
        get_soup_stuff(item,time_args,image_args,date_format)
        q.task_done()
        
def smbc_worker():
    time_args=list('div', {'class': 'cc-publishtime'})
    image_args=list('img',{'id': 'cc-comic'})
    worker(time_args, image_args, date_format)

# Create the queue and thread pool.
q = Queue()
for i in range(8):
    t = threading.Thread(target=smbc_worker)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()

def get_smbc_threaded():
    r = urllib.request.urlopen('http://www.smbc-comics.com/').read()
    soup = BeautifulSoup(r)
    
    counter=0
    prev_url=""
    
    while True:
        if (counter % 100 == 0):
            print("Finished "+str(counter) + " pages")
        q_item=soup
        q.put(q_item)
        try:
            prev_comic_soup = soup.find('a',{'rel': 'prev'})
            if prev_comic_soup["href"]==prev_url:
                break
            r = urllib.request.urlopen(prev_comic_soup["href"]).read()
            soup = BeautifulSoup(r)
            prev_url=prev_comic_soup["href"]
            counter+=1
        except:
            print(prev_url)
            #print(prev_comic_soup["href"])
            break
        

    
start = time.perf_counter() 
get_smbc_threaded()

q.join()       # block until all tasks are done

# "Work" took .1 seconds per task.
# 20 tasks serially would be 2 seconds.
# With 4 threads should be about .5 seconds (contrived because non-CPU intensive "work")
print('time:',time.perf_counter() - start)



#save_obj(csv_string, "delete")


with open("/Users/zburchill/Desktop/smbc_dates_threaded.csv","w") as f:
    f.write(csv_string)    
print(len(csv_string.splitlines()))
