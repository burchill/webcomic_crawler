

## Required reading ;)

Right now, to get up to date, check out `web_scraper_threaded_general.py` for the basic functions, and `comic_archive.py` for how I'm currently dealing with the archive of finished webcomics.  The file `auto_crawler.py` is where I was starting work on the automated web crawler, but then I found some other potential options.

# The general idea

### Web scraping

It's pretty easy to adjust a few little parameters to make something that collects the time data we want from a webcomic. (If you didn't already check the source files on the blog post on my website, you can check the basic implementation of the threaded code there.  I've actually written a lot of comments in the code, so you can understand it better. For the slightly more advanced version, check `web_scraper_threaded_general.py`.) You just need to know where the "next" button is, where they put their time in the HTML, and that's it, I think.  I've written a web scraper that will go through and collect all the relevant data. It opens specific links on a page, moves to them, gets data, opens another link, and repeats the process.

## Automatic web crawling

But we need more than just a few webcomics.  **In some ways, each webcomic is only going to have a single relevant datapoint** (i.e. the last time it updated) **so we need to get a lot**.  The one datapoint thing isn't 100% true, but I believe the type of model we'd want to means it's basically true. Hand-coding each webcomic would be pretty tedious, even if we made a GUI.  However, it's relatively easy, and relatively cool, to make something that would do this automatically.  If we had something like this, we could apply the model to all sorts of content creator data sets, like Youtubers, etc.

## Building a directed graph of a webcomic

My first idea was to make a web scraper that would get all the links on a page that stayed on that site and that it hadn't been to before, log all the connections between the current page and these links (as well as data currently on the page), and then open them all up and do the same thing.  In essence, creating a directed graph of the site.  With a few prior assumptions, you could generally use this structure to automatically get all the pages that were comic posts, rather than links to the store, etc.

You could imagine that most graphs of websites would be like what we see below.  Each oval is a page, and the red lines are the links.  Just from that structure, you could get a good idea about where the actual comics are--they're a long bidirectional chain in the graph. Not shown are the directions of the connections in the graph, which would make it even easier to recognize.  A link to the store page will be on almost all the comic pages, but other than the first and last comics, the store page probably won't link to any other comic pages.  

If we also put the constraint on this graph that the links between actual comic pages should be found in the same CSS/HTML areas, e.g., the arrows to navigate through the posts, it should be pretty dang assured for most comics.

![Directionality not shown](https://github.com/burchill/webcomic_crawler/raw/master/directed_graph.png)

### Using scrapy

In my research, I found a bunch of useful links:

 * http://stackoverflow.com/questions/10713230/how-can-i-make-a-graph-of-a-website-in-python
 * https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html
 * https://doc.scrapy.org/en/1.3/intro/overview.html
 * https://doc.scrapy.org/en/1.3/topics/architecture.html#topics-architecture
 * https://twistedmatrix.com/documents/current/core/howto/defer-intro.html

The gist of this is that there's already a seemingly easy-to-use web crawler package for Python, as well as a package for graph building / analysis.  The web crawler, `scrapy`, is built on some weird asychronous shit called `twisted`, which we might need to use if we can't use out-of-the-box stuff for `scrapy`.  I don't think it would be hard to modify what I already have, though.

## Push it to the limit

What would be another cool project in and of itself, would be to get all these graphs, and then use machine learning so that the graph analysis algorithm learns to find the comic pages by itself.  Presumably all we'd need is labelled data and some basic supervised learning algorithm.  I'm not an expert on that, but I bet any of our CS friends from high school would know.
