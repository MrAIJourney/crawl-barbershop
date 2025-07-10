import requests
from bs4 import BeautifulSoup
import json

def fetch_products_urls():
    """
    Fetches the URLs of all barbershop locations from the main page.
    Returns a list of URLs.
    """
    # Get products url from config.json file
    url = ''
    file = 'config.json'
    with open(file, 'r') as f:
        config = json.load(f)
        url = config.get('products_url')
    print('url:', url)



    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'div' tags with the class 'item'
    a_tags = soup.find_all('a', class_='btn-tgr-black selectProductButton')

    # Extract all 'a' tags inside each 'div' with class 'item'
    links = []
    for a_tag in a_tags:
        if a_tag and a_tag.get('href') and 'https://www.tedsgroomingroom.com/shop/products' in a_tag.get('href'):
            links.append(a_tag.get('href'))

    return links


def fetch_treatments_details(url):
    # Send a GET request to fetch the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create a dictionary to store the information
    products_details = {}

    # Extract name of the barbershop
    products_details['product name'] = soup.find('h1', class_='futura-pt-demi productName').text.strip() if soup.find('h1',
                                                                                                class_='futura-pt-demi productName') else 'N/A'

    # Extract price (from the "price" class in the page)
    price_element = soup.find('p', class_='price')
    products_details['price'] = price_element.text.strip() if price_element else 'N/A'

    # Extract short description
    short_desc_element = soup.find('p', class_='shortDescription')
    products_details['Short Description'] = short_desc_element.text.strip() if short_desc_element else 'N/A'

    # Extract long description
    long_desc_element = soup.find('p', id= 'longDescription')
    products_details['long description'] = long_desc_element.text.strip() if long_desc_element else 'N/A'

    # Extract beniefits section
    benefits_element = soup.find('div', id='benefits')
    benefit_paragraphs = benefits_element.find_all('p') if benefits_element else []
    products_details['benefits'] = [p.text.strip() for p in benefit_paragraphs] if benefit_paragraphs else 'N/A'

    # Extract usage section
    usage_element = soup.find('div', id='usage')
    usage_paragraphs = usage_element.find_all('p') if usage_element else []
    products_details['usage'] = [p.text.strip() for p in usage_paragraphs] if usage_paragraphs else 'N/A'

    # Extract ingredients section
    ingredients_element = soup.find('div', class_='card card-body')
    products_details['ingredients'] = ingredients_element.text.strip() if ingredients_element else 'N/A'

    # Extract UrL of the barbershop
    products_details['page_url'] = url

    return products_details


def save_to_json(data, filename='products_details.json'):
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
    print("All Products details saved to 'products_details.json'.")


def main():
    # List of URLs to scrape
    url_list = fetch_products_urls() # Fetch URLs from the location page
    # print(url_list)
    scrape_multiple_urls(url_list)


if __name__ == "__main__":
    main()
