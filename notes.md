

#The Plan

So who's who and what we gonna do? As far as I (Andrew) know now, there are just two people involved with this project (although I'm pretty sure more might be added):
* Zach Burchill
 * Skills: python, R, too much free time
* Andrew Burchill
 * Skills: genius, R, double genius (isn't super familiar with python)

However, we need to figure out exactly what needs to be done and who's going to do it.

##Things to do:

 * Filler
 * Be magic
 * Ask webtoons.com or tapastic.com for their data.  Just straight up email them and ask for the meta-data of some sampling of their comics.  We'd need post times, genre, and a few metrics of getting popularity.

##Notes, comments, other news

If you want to get TONS of webcomics incredibly rapidly (perhaps without the intelligent part of any of this), then check out [http://www.webtoons.com/en/](http://www.webtoons.com/en/). They're all on the same system, so it'll be darn easy to get data from them.

## Unread new/comments ---------------------------------------------------

Ok, given that you suck at Python evidently, let's focus on getting some preliminary data first and then you can get working on the model in R or something.  The problem with using webtoons is that we don't know 



## Small mini-projects

 * Harvest the webtoons.com / https://tapastic.com/ data.  We won't really know whether a comic is "dead" or not, but it will help anyway.  It would also help you learn how to use the web scraper I made so far.  Probably the best way for you to do this would be to get it so that it scrapes **one** comic first (e.g., owlturd/"blue chair").  Once you get that working, then you should know enough so that you can scrape http://www.webtoons.com/en/challenge/list?listType=league&genre=ALL&sortOrder=LIKEIT for, like, links to the top 500 webcomics, and then scrape those individually.
 * [Read how `networkx` works](https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html).  (I don't know it any better than you, and you don't need to know more than minimal Python anyway)
 * [Go through the incredibly easy `scrapy` tutorial](https://doc.scrapy.org/en/1.3/intro/tutorial.html)
 * 

## Quick intro to my scraper

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is really easy to learn, and very simple.  It just takes an HTML page and turns it into a tree based on the structure of the HTML elements.  Each element is a node, and all the elements in that node are its children nodes.  After you turn a webpage into the tree (called a soup, I guess) you can just search it for the elements you want.

Although the `web_scraper.py` file is my _old_ version, it might make things more clear. It's less flexible than the new one.  But let's look at how it gets the Broodhollow comic (`get_broodhollow()`).

This loads the comic and turns it into a soup object:

```python
def get_broodhollow():
    r = urllib.request.urlopen('http://broodhollow.chainsawsuit.com/').read()
    soup = BeautifulSoup(r)
```

 This sets the date format so that it can turn a string of the date into an actual date, and labels the two columns that will be used in the .csv file:
    
```python    
    date_format="%B %d, %Y"
    date_csv_s="post_date,cadavre"
    prev_url=""
 ```
 
This starts a loop, and the next line gets the date from the page:

```python
    while (True):
        date = datetime.strptime(soup.find(brood_is_date).contents[0],date_format)
```

That last line uses `soup.find(x)` to find the first element of the page (i.e. `soup`) which meets the right criteria supplied by `x`.  `soup.find_all(x)` does the same thing, but finds all instances in the page.  From the beautiful soup docs, you can see examples of what `x` can be, and what is returned

```python
soup.find_all("title")
# [<title>The Dormouse's story</title>]

soup.find_all("p", "title")
# [<p class="title"><b>The Dormouse's story</b></p>]

soup.find_all("a")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find_all(id="link2")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
```

The first one was a string, and returns elements of that type.  The second one is two strings: the first designates the element, and the second designates the class.  The third shows multiple results, and the fourth should that you can give it arbitrary key-value pairs.  If you wanted you could get a link specifically to fuck.com (e.g., `<a href="fuck.com" ...>`) with `soup.find_all(href="fuck.com")`.  You can also give `soup.find` and `soup.find_all` functions, however, which is what I do because it lets me be more flexible when I need it.

We can can see that I did this by passing in function `brood_is_date` to `soup.find`, which is defined as:

```python
def brood_is_date(x):
    try: 
        answer = x.name == "span" and x["class"]==["post-date"]
        return(answer)
    except: return(False)
```

Ignore the `try` statement, I did that to be more pythonic.  Trying to access `x["class"]` when the element doesn't have a class would cause an error, so I follow the principle of asking for forgiveness rather than permission.

The functions returns `True` for any element that is a `span` element and a `"class"` of `"post-date"`.  E.g., in Broodhollow, `<span class="post-date">October 27, 2016</span>`.  After getting it with `find`, I access its contents, which is a string in this case, and convert the time.  

Next, I do something similar to find the title with `brood_is_title`, so I can see if it's a Cadavre comic. Then I add a line to the string that will be written to the `.csv` file:

```python
        title_text = list(soup.find(brood_is_title).strings)[0]
        is_cadavre="cadavre" in title_text or "Cadavre" in title_text
        date_csv_s+="\n"+date.strftime("%x")+","+str(is_cadavre)
```

Finally, I try to load the next (in this case, "previous") comic, and if there isn't one, break out of the loop.  If there's an error, I also break out of the loop.

```python        
        try:
            prev_comic_soup = soup.find_all(brood_is_prev_comic)[0]
            if prev_comic_soup["href"]==prev_url:
                break
            r = urllib.request.urlopen(prev_comic_soup["href"]).read()
            soup = BeautifulSoup(r)
            prev_url=prev_comic_soup["href"]
        except:
            print(prev_url)
            print(prev_comic_soup["href"])
            break
```

Then I write the string to the .csv file:

```python
    with open("/Users/zburchill/Desktop/broodhollow_dates.csv","w") as f:
        f.write(date_csv_s)    
    print(len(date_csv_s.splitlines()))

```

### With threads

The threaded version (`web_scraper_threaded_general.py`) is very similar, but uses threads and is written to be more adaptable.  You can see how that changes things.  Just modify it based on the examples given to scrape something else.  The important difference with threads is that there is a "global lock" which is so that two threads don't try to change the same variable at the same time.  The variable they're changing there is writing to the `csv_string` string, and so each time they want to access it they have to go through `csv_string_lock`.
