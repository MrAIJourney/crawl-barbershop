import requests
from bs4 import BeautifulSoup
import json

def fetch_location_urls():
    """
    Fetches the URLs of all barbershop locations from the main page.
    Returns a list of URLs.
    """
    # Get location url from config.json file
    url = ''
    file = 'config.json'
    with open(file, 'r') as f:
        config = json.load(f)
        url = config.get('location_url')
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


def fetch_barbershop_details(url):
    # Send a GET request to fetch the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create a dictionary to store the information
    barbershop_details = {}

    # Extract name of the barbershop
    barbershop_details['name'] = soup.find('h2', class_='futura-pt-demi').text.strip() if soup.find('h2',
                                                                                                class_='futura-pt-demi') else 'N/A'

    # Extract address (from the "address" class in the page)
    address_element = soup.find('div', id='address')
    barbershop_details['address'] = address_element.text.strip() if address_element else 'N/A'

    # Extract phone number (from the "tel" link)
    phone_element = soup.find('div', id='phone')
    barbershop_details['phone'] = phone_element.text.strip() if phone_element else 'N/A'

    # Extract open hours (from the "store-hours" class)
    hours_element = soup.find('p', id= 'openingHours')
    barbershop_details['open_hours'] = hours_element.text.strip() if hours_element else 'N/A'

    # Extract description (general description under "location-description")
    description_element = soup.find('div', class_='col-12 col-lg-6 right-col pt-5 pb-5 align-self-center')
    barbershop_details['description'] = description_element.text.strip() if description_element else 'N/A'

    # Extract UrL of the barbershop
    barbershop_details['url'] = url

    return barbershop_details


def save_to_json(data, filename='barbershop_details.json'):
    # Save the extracted details into a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def scrape_multiple_urls(url_list):
    all_details = []

    for url in url_list:
        print(f"Scraping {url}...")
        details = fetch_barbershop_details(url)
        all_details.append(details)

    # Save all details into a JSON file
    save_to_json(all_details)
    print("All barbershop details saved to 'barbershop_details.json'.")


def main():
    # List of URLs to scrape
    url_list = fetch_location_urls() # Fetch URLs from the location page
    print(url_list)
    scrape_multiple_urls(url_list)


if __name__ == "__main__":
    main()
