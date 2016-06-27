""" Library entry point """
import re, requests
from bs4 import BeautifulSoup
from urlparse import urlparse

_headers = {'Connection': "keep-alive",
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
		'Referer': "",
		'Host':"",
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6',
		'Upgrade-Insecure-Requests':'1',
		}

_cookie = None
proxies =  {'http':'http://127.0.0.1:1080', 'https':'http://127.0.0.1:1080'}

class CLScrape(object):
    """ Scraper object to hold data """
    def __init__(self, soup, url):
        """ Initialize and scrape """
	urlpiece =  urlparse(url)
	self.baseurl = urlpiece.scheme + "://" + urlpiece.hostname
	self.host = urlpiece.hostname
	self.url = url
        self.soup = soup
        self.title = ""
        self.attrs = {}
        self.time = {}
        self.message = ""
        self.images = []

        for func in [ self.get_title, self.get_attrs, self.get_time, self.get_conent, self.get_image , self.get_email]:
            try:
                func()
            except Exception as e:
                print e
    
    def parse_attr(self, attr):
        """ Parse a single attribute from the BeautifulSoup tag """
        name = self.get_text(attr).strip(' :')
        value = attr.b.text.strip()
        self.attrs[name] = value



    def parse_string(self, selector):
        """ Parse first string matching selector """
        return self.get_text(self.soup.select(selector)[0])

    def parse_int(self, selector):
        """ Extract one integer element from soup """
        return int(re.sub('[^0-9]', '', self.parse_string(selector)))

    def get_text(self, item):
        """ Non-recursively extract text from an item """
        return item.find(text=True, recursive=True).strip()

    def get_time(self):
        self.time = {"posted":"", "updated":""}
        select = ".postinginfo";
        for op_time in self.soup.select(select):
            if op_time.find(text=True).find("posted:") != -1:
                self.time['posted'] = op_time.time['datetime']
            elif op_time.find(text=True).find("updated:") != -1: 
                self.time['updated'] = op_time.time['datetime']

    def get_attrs(self):
        """get attributes 
        :returns: TODO

        """
        self.attrs = {}
        for attrgroup in self.soup.select('.attrgroup'):
            for attr in attrgroup('span'):
                if attr.b and attr.text != attr.b.text:
                    self.parse_attr(attr)
        for attr in self.soup.select('.bigattr'):
            self.parse_attr(attr)

    def get_title(self):
        """ Extract title from a listing. CL does it inconsistently, thus takes
        some extra effort """
        self.title = ""
        try:
            self.title = self.parse_string('#titletextonly').strip(' -')
            return ;
        except:
            pass
        #fallback mechanism(s)
        self.title = self.soup.find(class_='postingtitle').text.strip()

    def get_conent(self):
        """get text contents posted

        """
        selector = "#postingbody"
        self.message = "".join([k.strip() for k in self.soup.select(selector)[0].findAll(text=True, recursive=True)])
        pass

    def get_image(self):
        """get the picture
        :returns: TODO

        """
        self.images = []
        userbody = self.soup.select(".userbody");
        if not userbody:
            return 
        thumbs = userbody[0].select("#thumbs")
        if not thumbs:
            # single image
            self.images.append(userbody[0].figure.findAll("img"))
            return 
        for thumb in thumbs[0].select(".thumb"):
            self.images.append(thumb['href'])




        pass
    def get_email(self):
        """get email of the poster
        :returns: TODO

        """

	
	replylink = self.baseurl + self.soup.select('#replylink')[0]['href']
	html = requests.get(replylink, headers = _headers, cookies=_cookie,  proxies = proxies).text
	esoup = BeautifulSoup(html, "html.parser")

	self.email = esoup.select('.anonemail')[0].find(text=True)
        pass
    def get_phone_number(self):
        """get phone number of the poster
        :returns: TODO

        """
        pass

    def get_price(self):
        try:
            self.price = self.parse_int('.price')
        except:
            self.price = 'Unlisted'
        pass

def scrape_html(html):
    """ Return meta information about a video """
    return CLScrape(BeautifulSoup(html, "html.parser"), "http://www.baidu.com")


def scrape_url(url):
    """ Scrape a given url for information """
    urlpiece =  urlparse(url)
    baseurl = urlpiece.scheme + "://" + urlpiece.hostname
    host = urlpiece.hostname
    global _headers
    global _cookie
    _headers['Referer']  = baseurl;
    _headers['Host'] = host
#    req0 = requests.get(baseurl, headers = _headers)
#
    req = requests.get(url, headers = _headers, proxies = proxies)
    _cookie = req.cookies
    html = req.text

    return CLScrape(BeautifulSoup(html, "html.parser"),url)
