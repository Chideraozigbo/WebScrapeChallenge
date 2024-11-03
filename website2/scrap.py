#%%
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd
import re 



#%%
# Constants for the website to scrape and logging
log_file = "/Users/user/Documents/Webscraping Project/website2/web_scrap_log.txt"
time_format = '%Y-%m-%d %H:%M:%S'
url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
time_format = '%Y-%m-%d %H:%M:%S'
now = datetime.now()
time_str = now.strftime(time_format)
filename = f'/Users/user/Documents/Webscraping Project/website2/data/data_{time_str}.csv'

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
    time_str = now.strftime(time_format)
    with open(log_file, 'a') as f:
        f.write(f'{time_str} - {message}\n')
#%%

def extract_data_from_pages(url):
    """
    This function connects to a specified URL, retrieves the HTML content, and extracts the relevant data.
    It iterates through a range of page numbers to scrape multiple pages.

    Parameters:
    url (str): The base URL of the website to scrape.

    Returns:
    BeautifulSoup: A BeautifulSoup object containing the HTML elements of the extracted data.
                   Returns None if unable to connect to any page.
    """
    for i in range(1, 21):
        url_with_page_number = f'{url}?page={i}'
        response = requests.get(url_with_page_number)
        if response.status_code == 200:
            log_message(f'{time_str} - Successfully connected to URL: {url}')
            soup = BeautifulSoup(response.text, 'lxml')
            boxes = soup.find('div', class_='col-lg-9')
            log_message(f'Scraping page {i} from {url_with_page_number}')
            return boxes
        else:
            log_message(f'Failed to connect to URL: {url}')
            break
        

def extract_product_names(boxes):
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
    items = boxes.find_all('a', class_='title')
    for item in items:
        product_names.append(item.text.strip())
        log_message(f'{time_str} - Product name: {item.text.strip()}')
    return product_names

def extract_product_prices(boxes):
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
    prices = boxes.find_all('h4', class_='price float-end card-title pull-right')
    for price in prices:
        product_prices.append(price.text.strip())
        log_message(f'{time_str} - Product price: {price.text.strip()}')
    return product_prices
#%%
def extract_product_descriptions(boxes):
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
    descriptions = boxes.find_all('p', class_='description card-text')
    for description in descriptions:
        product_descriptions.append(description.text.strip())
        log_message(f'{time_str} - Product description: {description.text.strip()}')
    return product_descriptions
#%%
def extract_ratings(boxes):
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
    log_message(f'{time_str} - Extracting ratings from products')
    ratings = []
    rating_elements = boxes.find_all('p', {'data-rating': True})
    
    for rating_element in rating_elements:
        rating = rating_element.get('data-rating')
        ratings.append(rating)
        log_message(f'{time_str} - Product rating: {rating}')
    
    return ratings
           
#%%    
def extract_reviews(boxes):
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
    log_message(f'{time_str} - Extracting reviews from products')
    reviews = []
    review_elements = boxes.find_all('p', class_='review-count float-end')
    
    for review_element in review_elements:
        review_count = ''.join(filter(str.isdigit, review_element.text.strip()))
        reviews.append(review_count)
        log_message(f'{time_str} - Product reviews: {review_count}')
    
    return reviews
        
#%%    
def join(product_names, product_prices, product_descriptions, ratings, reviews):
    """
    Creates a pandas DataFrame from the extracted product data.

    This function combines the separate lists of product information into a single
    DataFrame for easier manipulation and analysis.

    Parameters:
    product_names (list): A list of strings containing the names of the products.
    product_prices (list): A list of strings containing the prices of the products.
    product_descriptions (list): A list of strings containing the descriptions of the products.
    ratings (list): A list of strings containing the ratings of the products.
    reviews (list): A list of strings containing the number of reviews for each product.

    Returns:
    pandas.DataFrame: A DataFrame containing all the product information, with columns
                      'Product Name', 'Product Price', 'Product Description', 'Rating', and 'Reviews'.
    """
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
    """
    Saves a pandas DataFrame to a CSV file.

    This function takes a pandas DataFrame and saves it to a CSV file at the specified
    location. It logs the start and completion of the saving process.

    Args:
        df (pandas.DataFrame): The DataFrame to be saved to CSV.
        filename (str): The path and name of the file where the CSV will be saved.

    Returns:
        None

    Note:
        This function does not return any value but performs the side effect of
        saving the DataFrame to a file and logging the process.
    """
    log_message(f'{time_str} - Saving DataFrame to CSV file: {filename}')
    # with pd.ExcelWriter(filename, mode='w') as writer:
    #     df.to_excel(writer, index=False, sheet_name='Products')
    df.to_csv(filename, index=False)
    log_message(f'{time_str} - DataFrame saved to csv file: {filename}')
    
#%%
def main():
    """
    Main function to orchestrate the web scraping process.

    This function performs the following steps:
    1. Extracts data from web pages
    2. Processes the extracted data (names, prices, descriptions, ratings, reviews)
    3. Verifies data integrity
    4. Combines data into a DataFrame
    5. Saves the data to a CSV file

    The function uses several helper functions to perform these tasks and logs the progress and any errors encountered.

    Parameters:
    None

    Returns:
    None

    Raises:
    Exception: If any error occurs during the execution of the function, it logs the error and re-raises it.
    """
    try:
        box = extract_data_from_pages(url)
        if box:
            product_names = extract_product_names(box)
            product_prices = extract_product_prices(box)
            product_descriptions = extract_product_descriptions(box)
            ratings = extract_ratings(box)
            reviews = extract_reviews(box)

            # Verify all lists have the same length
            if len(product_names) == len(product_prices) == len(product_descriptions) == len(ratings) == len(reviews):
                df = join(product_names, product_prices, product_descriptions, ratings, reviews)
                load_to_csv(df, filename)
                log_message(f'{time_str} - Data fetching and processing completed successfully')
            else:
                log_message(f'{time_str} - Error: Mismatched number of elements extracted')
                log_message(f'Products: {len(product_names)}, Prices: {len(product_prices)}, ' 
                          f'Descriptions: {len(product_descriptions)}, Ratings: {len(ratings)}, '
                          f'Reviews: {len(reviews)}')
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
