import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd
import re 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

# Constants for the website to scrape and logging
home_dir = "/Users/user/Documents/Webscraping Project/"
log_file = os.path.join(home_dir, "website3/web_scrap_log.txt")
time_format = '%Y-%m-%d %H:%M:%S'
url = 'https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops'
now = datetime.now()
time_str = now.strftime(time_format)
filename = os.path.join(home_dir, f'website3/data/data_{time_str}.csv')
driver_dir = '/Users/user/Desktop/vfd-webscrap/chromedriver-mac-x64/chromedriver'

with open(log_file, 'w') as f:
    f.write(f'{time_str} - Log cleared\n')

def log_message(message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write(f'{current_time} - {message}\n')

def extract_data_from_pages(url, max_pages=20):
    """
    This function extracts data from multiple pages of a website using Selenium and BeautifulSoup.
    It navigates through the pages, waits for AJAX content to load, and extracts the required data.

    Parameters:
    url (str): The URL of the website to scrape.
    max_pages (int, optional): The maximum number of pages to scrape. Default is 20.

    Returns:
    list: A list of BeautifulSoup objects representing the content of each page.

    Raises:
    Exception: If any error occurs during the scraping process.
    """
    service = Service(driver_dir)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    boxes = []
    current_page = 1

    try:
        while current_page <= max_pages:
            # Wait for the content to load
            time.sleep(3)
            log_message(f'Waiting for AJAX content to load on page {current_page}')

            # Wait for the product container to be visible
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-9')))

            # Get the current page content
            soup = BeautifulSoup(driver.page_source, 'lxml')
            box = soup.find('div', class_='col-lg-9')
            if box:
                boxes.append(box)
                log_message(f'Scraped page {current_page} from {url}')

            # Check if there's a next page button
            try:
                # Wait for pagination container to be present
                pagination = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination')))

                # Find all page buttons
                buttons = driver.find_elements(By.CSS_SELECTOR, 
                    '.pagination button.page-link:not(.active)')

                # Find the next page button (should have text of current_page + 1)
                next_button = None
                for button in buttons:
                    if button.text.strip() == str(current_page + 1):
                        next_button = button
                        break

                if next_button:
                    # Scroll the button into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)

                    # Click the button
                    driver.execute_script("arguments[0].click();", next_button)
                    log_message(f'Clicked next button to page {current_page + 1}')
                    current_page += 1

                    # Wait for the page content to update
                    time.sleep(2)
                else:
                    log_message("No more pages available")
                    break

            except Exception as e:
                log_message(f"Error navigating to next page: {str(e)}")
                break

    except Exception as e:
        log_message(f"Error during page extraction: {str(e)}")
    finally:
        driver.quit()

    return boxes

def extract_product_names(boxes):
    log_message(f'Extracting product names from div elements')
    product_names = []
    for box in boxes:
        items = box.find_all('a', class_='title')
        for item in items:
            product_names.append(item.text.strip())
            log_message(f'Product name: {item.text.strip()}')
    return product_names

def extract_product_prices(boxes):
    log_message(f'Extracting product prices from div elements')
    product_prices = []
    for box in boxes:
        prices = box.find_all('h4', class_='price')
        for price in prices:
            product_prices.append(price.text.strip())
            log_message(f'Product price: {price.text.strip()}')
    return product_prices

def extract_product_descriptions(boxes):
    log_message(f'Extracting product descriptions from div elements')
    product_descriptions = []
    for box in boxes:
        descriptions = box.find_all('p', class_='description')
        for description in descriptions:
            product_descriptions.append(description.text.strip())
            log_message(f'Product description: {description.text.strip()}')
    return product_descriptions

def extract_ratings(boxes):
    log_message(f'Extracting ratings from products')
    ratings = []
    for box in boxes:
        
        products = box.find_all('div', class_='product-wrapper')
        for product in products:
            
            ratings_div = product.find('div', class_='ratings')
            if ratings_div:
                # Count the number of star icons
                star_count = len(ratings_div.find_all('span', class_='ws-icon-star'))
                ratings.append(str(star_count))
                log_message(f'Product rating: {star_count}')
            else:
                ratings.append('0')
                log_message(f'Product rating: 0 (No ratings found)')
    return ratings



def extract_reviews(boxes):
    log_message(f'Extracting reviews from products')
    reviews = []
    for box in boxes:
        review_elements = box.find_all('p', class_='review-count')
        for review_element in review_elements:
            review_count = ''.join(filter(str.isdigit, review_element.text.strip()))
            reviews.append(review_count)
            log_message(f'Product reviews: {review_count}')
    return reviews

def join(product_names, product_prices, product_descriptions, ratings, reviews):
    """
    Create a pandas DataFrame from extracted product data.

    This function combines various lists of product information into a single DataFrame.
    It logs the creation process using a custom logging function.

    Parameters:
    product_names (list): A list of product names.
    product_prices (list): A list of product prices.
    product_descriptions (list): A list of product descriptions.
    ratings (list): A list of product ratings.
    reviews (list): A list of product review counts.

    Returns:
    pandas.DataFrame: A DataFrame containing the combined product information
                      with columns for name, price, description, rating, and reviews.
    """
    log_message(f'Creating a DataFrame from extracted data')
    df = pd.DataFrame({
        'Product Name': product_names,
        'Product Price': product_prices,
        'Product Description': product_descriptions,
        'Rating': ratings,
        'Reviews': reviews
    })
    log_message(f'DataFrame created')
    return df

def load_to_csv(df, filename):
    """
    Save a pandas DataFrame to a CSV file.

    This function takes a DataFrame and saves it to a specified CSV file. It logs the
    start and completion of the saving process.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be saved to CSV.
    filename (str): The path and name of the CSV file where the DataFrame will be saved.

    Returns:
    None

    Side effects:
    - Creates or overwrites a CSV file at the specified filename.
    - Logs messages about the saving process.
    """
    log_message(f'Saving DataFrame to CSV file: {filename}')
    df.to_csv(filename, index=False)
    log_message(f'DataFrame saved to csv file: {filename}')

def main():
    """
    Execute the main web scraping process.

    This function orchestrates the entire web scraping operation. It extracts data from web pages,
    processes the extracted information, and saves it to a CSV file. The function handles potential
    errors and logs the progress of the operation.

    The function performs the following steps:
    1. Extract data from web pages
    2. Extract specific information (names, prices, descriptions, ratings, reviews)
    3. Verify data integrity
    4. Join the extracted data into a DataFrame
    5. Save the DataFrame to a CSV file

    No parameters are required as it uses global variables defined elsewhere in the script.

    Returns:
        None

    Raises:
        Exception: Any exception that occurs during the scraping process is logged and re-raised.
    """
    try:
        boxes = extract_data_from_pages(url)
        if boxes:
            product_names = extract_product_names(boxes)
            product_prices = extract_product_prices(boxes)
            product_descriptions = extract_product_descriptions(boxes)
            ratings = extract_ratings(boxes)
            reviews = extract_reviews(boxes)

            if len(product_names) == len(product_prices) == len(product_descriptions) == len(ratings) == len(reviews):
                df = join(product_names, product_prices, product_descriptions, ratings, reviews)
                load_to_csv(df, filename)
                log_message(f'Data fetching and processing completed successfully')
            else:
                log_message(f'Error: Mismatched number of elements extracted')
                log_message(f'Products: {len(product_names)}, Prices: {len(product_prices)}, ' 
                          f'Descriptions: {len(product_descriptions)}, Ratings: {len(ratings)}, '
                          f'Reviews: {len(reviews)}')
        else:
            log_message(f'Failed to fetch data from URL: {url}')
        log_message(f'Program completed and terminated')
    except Exception as e:
        log_message(f'An error occurred: {str(e)}')
        log_message(f'Program terminated')
        raise e

if __name__ == "__main__":
    main()