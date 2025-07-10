import requests
from bs4 import BeautifulSoup
import json

def fetch_treatments_urls():
    """
    Fetches the URLs of all barbershop locations from the main page.
    Returns a list of URLs.
    """
    # Get location url from config.json file
    url = ''
    file = 'config.json'
    with open(file, 'r') as f:
        config = json.load(f)
        url = config.get('treatments_url')
    print('url:', url)



    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'div' tags with the class 'item'
    divs = soup.find_all('div', class_='item col-12 col-lg-6')

    # Extract all 'a' tags inside each 'div' with class 'item'
    links = []
    for div in divs:
        a_tag = div.find('a')
        if a_tag and a_tag.get('href') and 'https://' in a_tag.get('href'):
            links.append(a_tag.get('href'))

    return links


def fetch_treatments_details(url):
    # Send a GET request to fetch the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create a dictionary to store the information
    treatments_details = {}

    # Extract name of the barbershop
    treatments_details['product name'] = soup.find('h1', class_='futura-pt-demi productName').text.strip() if soup.find('h1',
                                                                                                class_='futura-pt-demi productName') else 'N/A'

    # Extract price (from the "price" class in the page)
    price_element = soup.find_all('p', class_='price')
    price_list = []
    if price_element:
        for element in price_element:
            price_list.append(element.text.strip())
        treatments_details['price'] = price_list
    else:
        # If no price element is found, set to 'N/A'
        treatments_details['price'] = 'N/A'


    # Extract short description
    short_desc_element = soup.find('p', class_='shortDescription')
    treatments_details['Short Description'] = short_desc_element.text.strip() if short_desc_element else 'N/A'

    # Extract booking URL
    booking_element = soup.find('div', class_='buttonsC')
    booking_link = booking_element.find('a')
    if booking_link and booking_link.get('href'):
        treatments_details['booking_url'] = booking_link = booking_link.get('href')
    else:
        treatments_details['booking_url'] = 'N/A'

    # Extract long description
    long_desc_element = soup.find('p', id= 'longDescription')
    treatments_details['long description'] = long_desc_element.text.strip() if long_desc_element else 'N/A'


    # Extract UrL of the barbershop
    treatments_details['page_url'] = url

    return treatments_details


def save_to_json(data, filename='treatments_details.json'):
    # Save the extracted details into a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def scrape_multiple_urls(url_list):
    all_details = []

    for url in url_list:
        print(f"Scraping {url}...")
        details = fetch_treatments_details(url)
        all_details.append(details)

    # Save all details into a JSON file
    save_to_json(all_details)
    print("All treatments details saved to 'treatments_details.json'.")


def main():
    # List of URLs to scrape
    url_list = fetch_treatments_urls() # Fetch URLs from the location page
    scrape_multiple_urls(url_list)


if __name__ == "__main__":
    main()
