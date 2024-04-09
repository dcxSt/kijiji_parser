# https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/4+1+2__4+1+2+et+coin+detente__5+1+2__5+1+2+et+coin+detente/c37l1700281a27949001?sort=dateDesc&radius=2.0&price=__2600&address=M%C3%A9tro+Laurier%2C+Avenue+Laurier+Est%2C+Montr%C3%A9al%2C+QC&ll=45.52783749999999%2C-73.5889662


import requests
import re
from bs4 import BeautifulSoup

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

def parse_list_items(html_content):
    # Pattern to find <li></li> tags. This simplistic pattern assumes no nested tags within <li>
    pattern = re.compile(r'<li>(.*?)<\/li>', re.DOTALL)
    items = pattern.findall(html_content)
    return items

def get_listings(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    # Find all <section> elements with 'data-testid="listing-price"' attribute
    sections = soup.find_all('section', attrs={'data-testid': 'listing-card'})
    return [str(section) for section in sections]


def parse_listing_price(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    # Find all <p> elements with the specific data-testid attribute
    prices = soup.find_all('p', {'data-testid': 'listing-price'})
    # Extract and return the text content of these elements
    return [price.text for price in prices]

def parse_element(html_content, element_type:str, attrs:dict):
    soup = BeautifulSoup(html_content, 'lxml')
    els = soup.find_all(element_type, attrs=attrs)
    els = [el.text for el in els]
    if len(els)==0:
        return False
    elif len(els)==1:
        return els[0]
    return els

def get_href(html_content, element_type:str, attrs:dict):
    soup = BeautifulSoup(html_content, 'lxml')
    links = soup.find_all(element_type, attrs=attrs)
    hrefs = [link.get('href') for link in links if link.has_attr('href')]
    if len(hrefs)==0:
        return False
    elif len(hrefs)==1:
        return hrefs[0]
    return hrefs


def parse_listing(html:str):
    html
    listing = {
            "price":parse_element(html,'p',{'data-testid':'listing-price'}),
            "title":parse_element(html,'h3',{'data-testid':'listing-title'}),
            "description":parse_element(html,'p',{'data-testid':'listing-description'}),
            "link":get_href(html,'a',{'data-testid':'listing-link'}),
            "details":parse_element(html,'div',{'data-testid':'listing-details'}),
            #"date":parse_element(html,'p',{'data-testid':'listing-date'}),
            }
    return listing


"""
"""



if __name__ == "__main__":
    url = "https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/4+1+2__4+1+2+et+coin+detente__5+1+2__5+1+2+et+coin+detente/c37l1700281a27949001?sort=dateDesc&radius=2.0&price=__2600&address=M%C3%A9tro+Laurier%2C+Avenue+Laurier+Est%2C+Montr%C3%A9al%2C+QC&ll=45.52783749999999%2C-73.5889662"
    content = fetch_url_content(url)
    #listings = parse_listing_cards(content)
    #print(listings)
    #print(len(listings))
    listings = get_listings(content)
    parsed_listings = [parse_listing(l) for l in listings]
    print(parsed_listings)
    #print(len(listings))
    #for l in listings:
    #    price_text = parse_listing_price(l)
    #    print(price_text)
    ##print(listings)

    ##print(len(listings))

