

# Required reading ;)

Right now, to get up to date, check out `web_scraper_threaded_general.py` for the basic functions, and `comic_archive.py` for how I'm currently dealing with the archive of finished webcomics.  The file `auto_crawler.py` is where I was starting work on the automated web crawler, but then I found some other potential options.

# The general idea

So, if you didn't already check the source files on the blog post on my website, you can check the basic implementation of the threaded code there.  I've actually written a lot of comments in the code, so you can understand it better.  For the slightly more advanced version, check `web_scraper_threaded_general.py`.

Basically, it's pretty easy to adjust a few little parameters to make something that collects the time data we want from a webcomic.  You just need to know where the "next" button is, where they put their time in the HTML, and that's it, I think.  **However, in some ways, each webcomic is only going to have a single relevant datapoint** (i.e. the last time it updated) **so we need to get a lot**.  This makes hand-coding each webcomic pretty tedious.

## 
