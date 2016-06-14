import requests
from bs4 import BeautifulSoup
import json
import re
import unicodedata
import urllib2
from app.models import Admin

# TODO move this to utils
def handleUnicode(text):
    if isinstance(text, str):
        text = unicode(text, "latin-1")
    return unicodedata.normalize("NFKD", text).encode('utf-8')

def prepareSoup(url):
    response = requests.get(url)
    if response.status_code != 200:
        # NOTE 503s started appearing recently for amazon.
        # TODO re-iterate this with tinyproxy
        return {'status':'error', 'code': response.status_code}
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def crawlAuthor(url):
    soup = prepareSoup(url)
    if isinstance(soup, dict):
        return {'status': False}
    cards = soup.findAll('li', {'class': 'a-carousel-card'})
    for card in cards:
        link = card.find('a', {'class':'a-link-normal'})
        if link:
            item_link = link.attrs['href']
            item_link = item_link if 'amazon.in' in item_link else 'http://www.amazon.in'+item_link
            data = getAggregatedBookDetails(item_link)
            if not(data['amazon']) or ('status' in data['goodreads'] and data['goodreads']['status'] == 'error'):
                continue
            Admin.insertItem(data)
    return {'status': True}

def getAggregatedBookDetails(amzn_url):
    book_data = {'amazon': {}, 'goodreads': {}}
    book_data['amazon'] = AmazonCrawler(url=amzn_url).crawlPage()
    if book_data['amazon']:
        amazon_isbn = book_data['amazon']['isbn_13'] if 'isbn_13' in book_data['amazon'] else ''
        book_data['goodreads'] = GoodreadsCrawler(isbn=amazon_isbn).startCrawl()
        if 'status' in book_data['goodreads'] and book_data['goodreads']['status'] == 'error':
            amazon_isbn = book_data['amazon']['isbn_10'] if 'isbn_10' in book_data['amazon'] else ''
            book_data['goodreads'] = GoodreadsCrawler(isbn=amazon_isbn).startCrawl()
            if 'status' in book_data['goodreads'] and book_data['goodreads']['status'] == 'error':
                book_data['goodreads'] = GoodreadsCrawler(title=book_data['amazon']['title']).startCrawl()
    return book_data
 
class AmazonCrawler():
    def __init__(self, url='', title=''):
        self.url = url
        self.title = title

    def crawlPage(self):
        response = prepareSoup(self.url)
        if isinstance(response, dict):
            return {}
        isbn13, isbn10 = '',''
        detail_div = response.find('div', {'id': 'detail_bullets_id'})
        detail_list = detail_div.findAll('li')
        for detail in detail_list:
            if 'ISBN-13' in detail.text:
                isbn13 = detail.text.replace('ISBN-13:','').replace('-','').strip()
            if 'ISBN-10' in detail.text:
                isbn10 = detail.text.replace('ISBN-10:','').replace('-','').strip()

        amazon_id = 0
        book_id = response.find('input',{'id':'ASIN'})
        if book_id:
            amazon_id = book_id.attrs['value']

        title = response.find('span', {'id':'productTitle'})
        title = title.text if title else ''

        offer_price, striked_price = self.extract_price_data(response)                
        img_small, img_large = self.extract_images(response)
        
        rating = response.find("div", {"id":"avgRating"})
        rating = rating.text if rating else ""                
        if rating != "" and rating != None:
            rating = float(rating.split("out")[0].strip())

        num_reviews = 0
        num_reviews = response.find("a", {"class": "a-link-emphasis a-nowrap"})
        if num_reviews:
            num_reviews = re.search('\d+',num_reviews.text)
            if num_reviews:
                num_reviews = num_reviews.group(0)
        
        amzn_summary = self.findSummary(response)

        data = {
            'amazon_id': amazon_id,
            'title': title,
            'isbn_13': isbn13,
            'isbn_10': isbn10,
            'offer_price': offer_price,
            'list_price': striked_price,
            'img_small': img_small,
            'img_large': img_large,
            'rating': rating,
            'amzn_num_ratings': num_reviews,
            'amzn_summary': amzn_summary
        }
        return data

    def extract_price_data(self, response):
        offer_price = response.find('span',{'class':'a-color-price'})
        if offer_price:
            offer_price = offer_price.text
            offer_price = offer_price.encode("ascii", "ignore")
            offer_price = offer_price.strip()
        else:
            offer_price = response.find('td', {'class':'a-color-price a-size-medium a-align-top'})
            if offer_price:
                offer_price = offer_price.text
                offer_price = offer_price.encode("ascii", "ignore")
                offer_price = offer_price.strip()
                
        striked_price = response.find('span', {'class': 'a-color-secondary a-text-strike'})
        if striked_price:
            striked_price = striked_price.text
            striked_price = striked_price.encode("ascii", "ignore")
            striked_price = striked_price.strip()

        return (offer_price, striked_price)

    def extract_images(self, response):
        img_small, img_large = '', ''
        image_json = response.find("img", {"class":"frontImage"})
        if image_json:
            image_json = image_json.attrs['data-a-dynamic-image']
            urls = json.loads(image_json).keys()
            for url in urls:
                if 'SY' in url:
                    img_small = url
                else:
                    img_large = url
        return (img_small, img_large)
   
    def findSummary(self, response):
        summaries = {}
        summaries['Paperback'] = self.extractSummary(response)
        other_versions = response.findAll('li', {'class': 'swatchElement unselected'})
        for version in other_versions:
            anchor = version.find('a')
            link = 'http://www.amazon.in' + anchor.attrs['href']
            version_response = requests.get(link)
            format_type = anchor.find('span').text
            format_type = " ".join(re.findall("[a-zA-Z]+", format_type))
            summaries[format_type] = self.extractSummary(BeautifulSoup(version_response.text, "html.parser"))
        return summaries

    def extractSummary(self, response):
        scripts = response.findAll('script')
        for script in scripts:
            if 'bookDesc_iframe' in script.text:
                group = re.search('bookDescEncodedData = "(.*)"', script.text)
                if group:
                    encoded_summary = urllib2.unquote(group.group(1))
                    summary_text = BeautifulSoup(encoded_summary, "html.parser") 
                    return summary_text.text
        return ""


class GoodreadsCrawler():
    def __init__(self, isbn='', url='', title=''):
        self.base_url = 'https://www.goodreads.com' 
        self.search_url = self.base_url+'/search?utf8=%E2%9C%93&query='
        self.isbn = isbn
        self.url = url
        self.title = title

    def makeUrl(self):
        if self.url:
            return self.url
        if self.isbn:
            return self.search_url+self.isbn
        if self.title:
            return self.search_url+self.title
        return None

    def startCrawl(self):
        url = self.makeUrl()
        if not url:
            return {'status':'error'}

        soup = prepareSoup(url)
        if isinstance(soup, dict):
            return {}
        if self.title:
            data = self.crawlSearchPage(soup)
        else:
            data = self.crawlItemPage(soup)
        return data

    def crawlSearchPage(self, soup):
        error = {'status': 'error', 'code': 'results not found'}
        trs = soup.find('table', {'class': 'tableList'}) 
        if not trs:
            return error 
        result = trs.find('tr')
        if not result:
            return error
        anchors = result.find('td').findAll('a')
        for anchor in anchors:
            if 'href' in anchor.attrs:
                self.isbn, self.title = '',''
                self.url = self.base_url+anchor.attrs['href']
                return self.startCrawl()
        return error

    def crawlItemPage(self, soup):
        gr_id = 0
        book_id = soup.find('input',{'id':'book_id'})
        if book_id:
            gr_id = book_id.attrs['value']
       
        title = ''
        title_el = soup.find("h1",{"id":"bookTitle"})
        if title_el:
            title = title_el.text
            title = re.sub('\(.*\)','',title)
            title = title.strip()            
        else: 
            return {'status': 'error', 'code': 'page not found'}

        # Author
        author_el = soup.find("a", {"class":"authorName"})
        author = author_el.text if author_el else ''
            
        # Average Rating
        avg_rating_el = soup.find("span",{"class":"value rating"})
        avg_rating = avg_rating_el.text if avg_rating_el else ''
    
        # Num ratings and reviewers 
        num_rating = ''
        num_review = ''
        meta_rating = soup.findAll("span",{"class":"value-title"})
        for meta in meta_rating:
            if 'itemprop' in meta.attrs:
                num_rating = meta.text
                num_rating = num_rating.lower().replace('ratings','').strip()
            else:
                num_review =  meta.text
                num_review = num_review.lower().replace('reviews','').strip()

        # Summary
        gr_summary = ""
        desc_container = soup.find('div', {'id': 'descriptionContainer'})
        if desc_container:
            summaries = desc_container.findAll('span')
            if summaries:
                gr_summary = summaries[-1]
                if gr_summary:
                    gr_summary = gr_summary.text

        # ISBNs, Language 
        isbn_10 = ''
        isbn_13 = ''
        language = ''
        pub_details = ''
        alt_title = ''
        series = ''
        awards = ''
        isbns = []
        other_meta_key = soup.findAll("div",{"class":"infoBoxRowTitle"})
        other_meta_value = soup.findAll("div",{"class":"infoBoxRowItem"})
        for i, key in enumerate(other_meta_key):
            if key.text == "Original Title":
                alt_title = other_meta_value[i].text.replace('\n','').strip()
            elif key.text == "ISBN":
                isbn_10 = other_meta_value[i].text.replace('\n','').strip()
                isbn_10 = isbn_10.replace(' ','')
                isbn_13_raw = re.search('\(ISBN13.*\)', isbn_10)
                if isbn_13_raw:
                    isbn_13_raw = isbn_13_raw.group(0)
                    isbn_13 = isbn_13_raw.replace('ISBN13:','').replace('(','').replace(')','')
                    isbn_10 = isbn_10.replace(isbn_13_raw, '')
            elif key.text == "Edition Language":
                language = other_meta_value[i].text.replace('\n','').strip()
            elif key.text == "Series":
                series  = other_meta_value[i].text.replace('\n','').strip()
            elif key.text == "Literary Awards":
                awards  = other_meta_value[i].text.replace('\n','').strip()
            elif "Other Editions" in key.text:
                anchor = key.find('a')
                if anchor:
                    isbns = self.getOtherISBNs(anchor.attrs['href'])
    
        # Book Binding
        bind_type = soup.find("span", {"itemprop":"bookFormatType"})    
        bind_type = bind_type.text if bind_type else ''

        # Edition
        edition = soup.find("span", {"itemprop":"bookEdition"})    
        edition = edition.text if edition else ''

        # Number of Pages
        num_page  = soup.find("span", {"itemprop":"numberOfPages"})    
        num_page = num_page.text if num_page else 0

        # Publisher Details (including 1st published)
        pub_el = soup.find("div", {"id":"details"})
        if pub_el:
            pub_el = pub_el.findAll("div", {"class":"row"})
            if pub_el:
                pub_el = pub_el[-1].text
                pub_details = pub_el.replace('\n',' ').replace('  ', '')
                # TODO format and extract

        # Genres
        genres = []
        genre_el = soup.findAll("div", {"class":"elementList"})
        if genre_el:
            for el in genre_el:
                genre = el.find("div",{"class":"left"})
                num_genre =  el.find("div",{"class":"right"})
                if genre:
                    genre_name = genre.text.replace('\n','').replace('  ','')
                    if '>' in genre_name:
                        genre_name = genre_name[genre_name.index('>')+1:]
                    genres.append([genre_name, num_genre.text.replace(' users','').replace('\n','')])

        # Handle unicode 
        title = handleUnicode(title)
        author = handleUnicode(author)
        pub_details = handleUnicode(pub_details)
        series = handleUnicode(series)
        awards = handleUnicode(awards)
        if isbn_13 in isbns:
            isbns.remove(isbn_13)

        data = {         
            'gr_id': gr_id,
            'title': title,
            'author': author,
            'avg_rating': avg_rating,
            'num_ratings':num_rating,
            'num_review': num_review,
            'isbn_10':    isbn_10,
            'isbn_13':    isbn_13,
            'language':   language,
            'bind_type':  bind_type,
            'edition':    edition,
            'num_page':   num_page,
            'pub_details':pub_details,
            'alt_title':  alt_title,
            'series':     series,
            'awards':     awards,
            'genres':     genres,
            'isbns':      isbns,
            'gr_summary': gr_summary
        }
        return data

    def getOtherISBNs(self, url):
        url = self.base_url+url
        resp = requests.get(url)
        if resp.status_code != 200:
            return []
        sub_soup = BeautifulSoup(resp.text, "html.parser")
        details = sub_soup.findAll('div', {'class':'moreDetails'})
        isbns = []
        for detail in details:
            if len(isbns) <= 5:
                values = detail.findAll('div', {'class': 'dataValue'})
                for value in values:
                    if 'ISBN13' in value.text:
                        find_isbn = re.search('\(ISBN13: (.*)\)', value.text) 
                        if find_isbn:
                            isbns.append(find_isbn.group(1))
            else:
                break
        return isbns
