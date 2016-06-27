from craigslist_scraper.scraper import scrape_url,scrape_html
#data = scrape_url('http://kootenays.craigslist.ca/mcy/5607706729.html')
def test(html):
    data = scrape_html(open(html).read())
    print  "title: ", data.title
    print "attrs: " ,data.attrs
    print "time: " ,data.time
    print "message: ", data.message
    print "images: ", data.images

for i in ['testAll.html', 'test2.html','5654187283.html' ]:
    print '===================>' , i
    test(i)
