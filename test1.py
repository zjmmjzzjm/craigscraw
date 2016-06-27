from craigslist_scraper.scraper import scrape_url,scrape_html
#data = scrape_url('http://kootenays.craigslist.ca/mcy/5607706729.html')
data = scrape_html(open('testAll.html').read())
print  "title: ", data.title
print "attrs: " ,data.attrs
print "time: " ,data.time
print "message: ", data.message
