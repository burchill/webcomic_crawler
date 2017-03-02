'''
Created on Jan 21, 2017

@author: zburchill
'''

from urllib.parse import urljoin 



# is the right way of getting links. First argument is site you're on, second is the link url
urljoin("http://www.asite.com/folder/baba/", "/anotherpage/")




m = urllib.request.urlopen("http://www.webtoons.com/challenge/episodeList?titleNo=3934")
m.geturl()
# 'http://www.webtoons.com/en/challenge/tea-party-an-american-story/list?title_no=3934'

# check out scrapy, dammit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# Troublesome, because some comics, such as those hosted on tapastic, will have the individual comics in subdirectories,
#    such as: 'https://tapastic.com/series/Lunarbaboon'.  For this reason, I think it would be wise to consider the original link to the site in question
#    For example, when the comic archive links to the comic, it should take that link to be the base directory. Anything going above it isn't on the same site
# Additionally: this should return 'False' for 'http://www.test.com' and 'http://test.com'
def check_if_on_same_site(original_url, new_url):
    