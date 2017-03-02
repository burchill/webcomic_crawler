

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

For example, after you turn a 
