# https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/4+1+2__4+1+2+et+coin+detente__5+1+2__5+1+2+et+coin+detente/c37l1700281a27949001?sort=dateDesc&radius=2.0&price=__2600&address=M%C3%A9tro+Laurier%2C+Avenue+Laurier+Est%2C+Montr%C3%A9al%2C+QC&ll=45.52783749999999%2C-73.5889662

import requests
import re
from bs4 import BeautifulSoup
import json
import os
import notification # pythonista module

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"

def get_listings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all <section> elements with 'data-testid="listing-price"' attribute
    sections = soup.find_all('section', attrs={'data-testid': 'listing-card'})
    return [str(section) for section in sections]

def parse_element(html_content, element_type:str, attrs:dict):
    """Return the body of a specific html element from it's attributes"""
    soup = BeautifulSoup(html_content, 'html.parser')
    els = soup.find_all(element_type, attrs=attrs)
    els = [el.text for el in els]
    if len(els)==0:
        return False
    elif len(els)==1:
        return els[0]
    return els

def get_href(html_content:str, element_type:str, attrs:dict):
    """Return the link of an element with specific attributes"""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all(element_type, attrs=attrs)
    hrefs = [link.get('href') for link in links if link.has_attr('href')]
    if len(hrefs)==0:
        return False
    elif len(hrefs)==1:
        return hrefs[0]
    return hrefs


def parse_listing(html:str):
    """:param html str: A string containing the html inside the listing <li> element.
    Return a dictionary with essential information about listing."""
    listing = {
            "price":parse_element(html,'p',{'data-testid':'listing-price'}),
            "title":parse_element(html,'h3',{'data-testid':'listing-title'}),
            "description":parse_element(html,'p',{'data-testid':'listing-description'}),
            "link":get_href(html,'a',{'data-testid':'listing-link'}),
            "details":parse_element(html,'div',{'data-testid':'listing-details'}),
            #"date":parse_element(html,'p',{'data-testid':'listing-date'}),
            }
    return listing

if __name__ == "__main__":
    ### Get kijiji page information
    url = "https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/4+1+2__4+1+2+et+coin+detente__5+1+2__5+1+2+et+coin+detente/c37l1700281a27949001?sort=dateDesc&radius=2.0&price=__2600&address=M%C3%A9tro+Laurier%2C+Avenue+Laurier+Est%2C+Montr%C3%A9al%2C+QC&ll=45.52783749999999%2C-73.5889662"
    content = fetch_url_content(url)
    listings = get_listings(content)
    parsed_listings = [parse_listing(l) for l in listings]
    ### Get locally stored listing information
    saved_listings = []
    LISTING_PATH = "listings.json"
    if os.path.exists(LISTING_PATH):
        with open(LISTING_PATH,"r") as f:
            saved_listings = json.loads(f.read()) 
    else:
        print("No listings saved, proceeding.")
    saved_links = [l['link'] for l in saved_listings]
    new_listings = [] # If this is not empty after update, we'll alert user
    # update then serialize saved_listings
    for listing in parsed_listings:
        if listing['link'] not in saved_links:
            saved_listings.append(listing)
            new_listings.append(listing)
    with open(LISTING_PATH,"w") as f:
        json.dump(saved_listings,f)
    if new_listings == []:
        print("No new listings found.")
    else:
        print("Listings updated, alerting user.")
        notification.schedule(
            title=f'New Listing ({len(new_listings)})',
            message="",
            delay=0, #seconds
            sound_name='default'
                )
        print(f"\nSearch url: {url}\n")
    for l in new_listings:
        print(f"title: {l['title']}")
        print(f"link: {l['link']}")
        print(f"price: {l['price']}\n")
    
