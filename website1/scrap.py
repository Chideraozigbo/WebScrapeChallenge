#%%
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd


#%%
# Constants for the website to scrape and logging
log_file = "/Users/user/Documents/Webscraping Project/website1/web_scraper_log.txt"
time_format = '%Y-%m-%d %H:%M:%S'
url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
max_retries = 3
retry_delay = 5  # seconds
time_format = '%Y-%m-%d %H:%M:%S'
now = datetime.now()
time_str = now.strftime(time_format)
filename = f'/Users/user/Documents/Webscraping Project/website1/data_{time_str}.csv'

#%%
# Clear previous log content
with open(log_file, 'w') as f:
    f.write(f'{time_str} - Log cleared\n')

def log_message(message):
    """
    Log a message to a file with a timestamp.

    Args:
        message (str): The message to be logged.
    """
    with open(log_file, 'a') as f:
        f.write(f'{time_str} - {message}\n')
#%%
def extract(url):
    """
    Attempts to fetch and extract data from a given URL with retry mechanism.

    This function tries to connect to the specified URL, fetch the HTML content,
    and extract a specific div element. It includes error handling and a retry
    mechanism for failed attempts.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        BeautifulSoup object or None: Returns a BeautifulSoup object containing
        the extracted div element if successful, or None if all attempts fail.

    Raises:
        No exceptions are raised as they are caught and logged internally.
    """
    log_message(f'Starting data fetch from URL: {url}')
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                log_message(f'{time_str} - Successfully connected to URL: {url}')
                soup = BeautifulSoup(response.text, 'lxml')
                box = soup.find('div', class_='col-lg-9')
                return box
            else:
                retries += 1
                log_message(f'{time_str} - Failed to connect to URL {url} - Status Code: {response.status_code} (Attempt {retries} of {max_retries})')
                if retries < max_retries:
                    log_message(f'{time_str} - Retrying in {retry_delay} seconds...')
                    time.sleep(retry_delay)
        except Exception as e:
            retries += 1
            log_message(f'{time_str} - Error while fetching URL {url}: {str(e)} (Attempt {retries} of {max_retries})')
            if retries < max_retries:
                log_message(f'{time_str} - Retrying in {retry_delay} seconds...')
                time.sleep(retry_delay)

    log_message(f'{time_str} - All attempts to fetch URL {url} failed after {max_retries} retries.')
    return None
#%%
def extract_product_names(box):
    """
    Extracts product names from a BeautifulSoup object containing HTML elements.

    This function searches for all 'a' tags with class 'title' within the given
    BeautifulSoup object, extracts the text content of each tag, and logs each
    product name found.

    Args:
        box (BeautifulSoup): A BeautifulSoup object containing HTML elements
                             from which to extract product names.

    Returns:
        list: A list of strings, where each string is a product name extracted
              from the HTML.

    """
    log_message(f'{time_str} - Extracting product names from div element')
    product_names = []
    items = box.find_all('a', class_='title')
    for item in items:
        product_names.append(item.text.strip())
        log_message(f'{time_str} - Product name: {item.text.strip()}')
    return product_names
#%%
def extract_product_prices(box):
    """
    Extracts product prices from a BeautifulSoup object containing HTML elements.

    This function searches for all 'h4' tags with specific classes within the given
    BeautifulSoup object, extracts the text content of each tag (which represents
    the price), and logs each price found.

    Args:
        box (BeautifulSoup): A BeautifulSoup object containing HTML elements
                             from which to extract product prices.

    Returns:
        list: A list of strings, where each string is a product price extracted
              from the HTML. The prices are stripped of leading and trailing whitespace.
    """
    log_message(f'{time_str} - Extracting product prices from div element')
    product_prices = []
    prices = box.find_all('h4', class_='price float-end card-title pull-right')
    for price in prices:
        product_prices.append(price.text.strip())
        log_message(f'{time_str} - Product price: {price.text.strip()}')
    return product_prices
#%%
def extract_product_descriptions(box):
    """
    Extracts product descriptions from a BeautifulSoup object containing HTML elements.

    This function searches for all 'p' tags with class 'description card-text' within the given
    BeautifulSoup object, extracts the text content of each tag, and logs each
    product description found.

    Args:
        box (BeautifulSoup): A BeautifulSoup object containing HTML elements
                             from which to extract product descriptions.

    Returns:
        list: A list of strings, where each string is a product description extracted
              from the HTML. The descriptions are stripped of leading and trailing whitespace.
    """
    log_message(f'{time_str} - Extracting product descriptions from div element')
    product_descriptions = []
    descriptions = box.find_all('p', class_='description card-text')
    for description in descriptions:
        product_descriptions.append(description.text.strip())
        log_message(f'{time_str} - Product description: {description.text.strip()}')
    return product_descriptions
#%%
def extract_ratings(box):
    """
    Extracts the rating from a BeautifulSoup object containing HTML elements.

    This function searches for a 'div' element with class 'ratings' within the given
    BeautifulSoup object, then looks for a 'p' element with a 'data-rating' attribute.
    If found, it extracts and returns the rating value.

    Args:
        box (BeautifulSoup): A BeautifulSoup object containing HTML elements
                             from which to extract the rating.

    Returns:
        str or None: The rating value as a string if found, or None if not found.
    """
    log_message('{time_str} - Extracting rating from div element')
    rating_div = box.find('div', class_='ratings')
    if rating_div:
        # Find the p element with data-rating attribute
        rating_p = rating_div.find('p', {'data-rating': True})
        if rating_p:
            ratings = rating_p.get('data-rating')
            log_message(f'{time_str} - Product rating: {ratings}')
            return ratings
        else:
            log_message('{time_str} - Product rating: Not found')
            return None
    else:
        log_message('{time_str} - Product rating div: Not found')
        return None
#%%    
def extract_reviews(box):
    """
    Extracts the number of reviews from a BeautifulSoup object containing HTML elements.

    This function searches for a 'p' element with class 'review-count float-end' within the given
    BeautifulSoup object. If found, it extracts the number of reviews from the text content.

    Args:
        box (BeautifulSoup): A BeautifulSoup object containing HTML elements
                             from which to extract the number of reviews.

    Returns:
        str or None: The number of reviews as a string if found, or None if not found.
                     The returned string contains only the digits from the review count.
    """
    log_message('{time_str} - Extracting reviews from div element')
    reviews_div = box.find('p', class_='review-count float-end')
    if reviews_div:
        # Extract number of reviews from the text
        reviews_text = reviews_div.text.strip()
        reviews = ''.join(filter(str.isdigit, reviews_text))  # Extract digits only
        log_message(f'{time_str} - Product reviews: {reviews}')
        return reviews
    else:
        log_message('{time_str} - Product reviews: Not found')
        return None
#%%    
def join(product_names, product_prices, product_descriptions, ratings, reviews):
    log_message(f'{time_str} - Creating a DataFrame from extracted data')
    df = pd.DataFrame({
        'Product Name': product_names,
        'Product Price': product_prices,
        'Product Description': product_descriptions,
        'Rating': ratings,
        'Reviews': reviews
    })
    log_message(f'{time_str} - DataFrame created')
    return df
#%%
def load_to_csv(df, filename):
    log_message(f'{time_str} - Saving DataFrame to CSV file: {filename}')
    # with pd.ExcelWriter(filename, mode='w') as writer:
    #     df.to_excel(writer, index=False, sheet_name='Products')
    df.to_csv(filename, index=False)
    log_message(f'{time_str} - DataFrame saved to csv file: {filename}')
    
#%%
def main():
    try:
        box = extract(url)
        if box:
            product_names = extract_product_names(box)
            product_prices = extract_product_prices(box)
            product_descriptions = extract_product_descriptions(box)
            ratings = [extract_ratings(box) for _ in product_names]
            reviews = [extract_reviews(box) for _ in product_names]
            df = join(product_names, product_prices, product_descriptions, ratings, reviews)
            load_to_csv(df, filename)
            log_message(f'{time_str} - Data fetching and processing completed successfully')
        else:
            log_message(f'{time_str} - Failed to fetch data from URL: {url}')
        log_message(f'{time_str} - Program completed and terminated')
    except Exception as e:
        log_message(f'{time_str} - An error occurred: {str(e)}')
        log_message(f'{time_str} - Program terminated')
        raise e


if __name__ == "__main__":
    main()

        


# %%
