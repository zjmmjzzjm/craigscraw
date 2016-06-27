""" Library entry point """
import re, requests
from bs4 import BeautifulSoup

class CLScrape(object):
    """ Scraper object to hold data """
    def __init__(self, soup):
        """ Initialize and scrape """
        self.soup = soup
        self.get_title()
        self.get_attrs()
        self.get_time()
        self.get_conent()
        self.get_image()
    

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
        select = ".postinginfo.reveal";
        k = 0
        for op_time in self.soup.select(select):
            k += 1
            if k == 1:
                continue
            elif k == 2:
                self.time['posted'] = op_time.time['datetime']
                pass
            elif k == 3:
                self.time['updated'] = op_time.time['datetime']
                pass

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
            picture = userbody[0].figure.findAll("img")
            print picture[0]['src']
            return 
        for thumb in thumbs[0].select(".thumb"):
            print thumb['href']




        pass
    def get_email(self):
        """get email of the poster
        :returns: TODO

        """
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
    return CLScrape(BeautifulSoup(html, "html.parser"))


def scrape_url(url):
    """ Scrape a given url for information """
    html = requests.get(url).text
    return scrape_html(html)
