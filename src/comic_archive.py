'''
Created on Nov 20, 2016

@author: zburchill
'''
import operator
import json
import re

# for threading
import threading
from queue import Queue
import time
from web_scraper_threaded_general import soupify, alexa_page_rank


# A test wrapper for soupify
def did_it_load(url_t):
    try:
        soup=soupify(url_t)
        return(True)
    except Exception as error_m:
        return(str(error_m)+" -- "+url_t)
        
def temp_wrapper(urls):
    def list_comp_f(url_t2):
        soup=soupify(url_t2)
        try:
            json_stuff=tap_tastic_json(soup)
        except IOError as error_m:
            if str(error_m)=="Can't read tapastic url":
                print("Url: "+url_t2+" unread by json!!!!")
                return(0)
            else:
                raise
        return(json_csv(json_stuff))
    csvs=[list_comp_f(e) for e in urls]
    csvs=[e for e in csvs if e]
    with open("/Users/zburchill/Desktop/tapastic.csv","w") as f:
        s=csvs[0]+"\n"
        s+="\n".join(["\n".join(e.splitlines()[1:]) for e in csvs[1:]])
        f.write(s)
    


# This is my incredibly hacky way of getting some of the data on the taptastic sites into the right json format
def tap_tastic_json_fixer(s):
    s=re.sub("^\s+}","}",s,flags=re.MULTILINE)
    s=re.sub("^\s+","\"",s,flags=re.MULTILINE) #adds quotation marks to first half of variables
    s=re.sub(" : ","\" : ",s) # adds quotation marks to second half
    s=re.sub(" : '"," : \"",s)
    s=re.sub("',(?=\s*$)","\",",s,flags=re.MULTILINE)
    s=re.sub(" //.+$","",s,flags=re.MULTILINE)
    s=re.sub("^\s*\"subscribers\".+$","",s,flags=re.MULTILINE)
    s=re.sub("\\\(?=[^\"\\\/tnru])","",s)
    return(s)

# More hacky code to find the data
def tap_tastic_json(soup_t):
    scripts=soup_t.find_all('script',{'type': 'text/javascript'})
    for script in scripts:
        try:
            if "episodeList" in script.string:
                json_string = script.string.strip().split(";")[0][12:]
                json_stuff=json.loads(tap_tastic_json_fixer(json_string))
                return(json_stuff)
#             lines = script.string.splitlines()
#             for line in lines:
#                 if "episodeList" in line:
#                     return(json.loads(line.split(" : ")[1][0:-1]))
#                     break
        except Exception as error_m:
            print("taptastic error: "+str(error_m))
    raise IOError("Can't read tapastic url")
    return(None)


# turning the taptastic json into csv formats
def json_csv(taptastic_json,
             add_name=True,
             args=["popularCnt","shareCnt","commentCnt","thumbsupCnt","publishDate"]):
    s=",".join(args)
    constants=""
    if add_name:
        constants=","+taptastic_json['seriesTitle']
        s+=",comicName"
    for post in taptastic_json['episodeList']:
        line="\n"+",".join([str(post[e]) for e in args])+constants
        s+=line
    return(s)
        

# We are not going to even try to scrape data from comics on these sites, for a variety of reasons
def nono_finder(url_t):
    list_of_nonos = ["furaffinity.net","facebook.com","deviantart.com","google.com","dropbox.com",
                     "http://niemann.blogs.nytimes.com/","photobucket.com/"]
    for nono in list_of_nonos:
        if nono in url_t:
            return(True)
    return(False)

# Is it a link element with the attribute "target"
def a_and_target(tag):
    return tag.name=="a" and tag.has_attr("target")

# Is it a "reader's choice" comic
def has_star(tag):
    if tag.find('em','star'):
        return(True)
    else: return(False)

# What are the warnings of explicit content?
def get_nsfw(tag):
    warn=tag.find('em','warn')
    if warn:
        return(warn.string)
    else: return("")


alexa_dict={}
alexa_dict_lock = threading.Lock()

# The worker thread pulls an item from the queue and processes it
def alexa_worker():
    while True:
        url = alexa_q.get()
        try:
            ranking=alexa_page_rank(url)
        except Exception as error_m:
            print("Error loading: "+url)
            print(str(error_m))
            ranking=999999999999999999999999
        with alexa_dict_lock:
            alexa_dict[url]=ranking
        alexa_q.task_done()
         
alexa_q = Queue()
for i in range(100): #IDK, i just picked that many threads. YOU should do it more principled?
    #t = threading.Thread(target=smbc_worker) # change this to what you make
    t = threading.Thread(target=alexa_worker) # change this to what you make
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()


def get_n_most_popular_comics(n):
    soup = soupify("http://new.belfrycomics.net/view/all/Inactive")
    ce_elements=soup.find_all('span', {'class':'ce'})
    link_elements=[e.find(a_and_target) for e in ce_elements]
    urls=[e['href'] for e in link_elements]
    start = time.perf_counter() 
    for e in urls:
        alexa_q.put(e)
    titles=[e.string for e in link_elements]
    stars=[has_star(e) for e in ce_elements]
    nsfw_markers=[get_nsfw(e) for e in ce_elements]
    alexa_q.join()  # wait till page ranks are done
    print('time:',time.perf_counter() - start)
    #rankings=[alexa_dict[e] for e in urls]
    sorted_x = sorted(alexa_dict.items(), key=operator.itemgetter(1))
    
    filtered_x=[e for e in sorted_x if not (nono_finder(e[0]))]
    tapastic=[e[0] for e in filtered_x if "tapastic" in e[0]]
#     temp_wrapper(tapastic)

    print(filtered_x[0:100])
    

get_n_most_popular_comics("a")







#print(soupify("https://tapastic.com/browse").find('ul',{'class':'page-list-wrap'}))