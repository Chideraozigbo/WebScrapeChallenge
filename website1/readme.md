# E-commerce Web Scraping Project

## Overview
This project focuses on scraping an e-commerce website to gather product information. The site includes multiple categories and subcategories, with all items loaded on a single page. This structure enables efficient extraction of product details such as name, price, rating, and review count.

The project serves as a foundational example of web scraping for e-commerce, providing a structured approach to collecting data for analysis or integration into data pipelines.

## Project Goals
1. **Extract Product Information**: Gather details like product name, price, rating, and reviews for each item on the page.
2. **Handle Dynamic Data**: Efficiently navigate and scrape data across various categories and subcategories.
3. **Data Storage**: Store the scraped data in structured formats (CSV or JSON) for easy analysis or further integration.

## Requirements

### Dependencies
Ensure the following Python libraries are installed:
- `requests` - For handling HTTP requests.
- `BeautifulSoup` - For parsing HTML and locating elements.
- `pandas` - For organizing and saving data in structured formats.
- `openpyxl` - For saving data to Excel files (if required).

Install the required libraries using the following command:
``` bash
pip install requests beautifulsoup4 pandas openpyxl
```

## Additional Requirements

- Python 3.7+
- Git for version control

## Project Structure
The project has the following structure:
``` bash
Webscraping Project/
├── website1/
│   ├── scrap.py 
│   └── data/ 
│       └── products.csv 
├── website2/
│   ├── scrap.py 
│   └── data/ 
│       └── products.csv
├── README.md                   # Project documentation
└── requirements.txt            # List of dependencies
```
## Setup and Usage
### Clone the Repository
First, clone the repository to your local machine:

``` bash
git clone https://github.com/Chideraozigbo/WebScrapeChallenge.git cd Webscraping Project 
```


### Run the Script
Navigate to the project directory and run the `scrap.py` script:

``` python 
python website1/scrap.py 
```


### Output
The script will:

1. Access the e-commerce webpage for all products in a category.
2. Extract product details like name, price, rating, and review count.
3. Save the data as a CSV file in the data folder.

## Logging
Log messages are generated throughout the extraction process to track key actions and events, including the start and completion of each extraction phase. Logs provide insights into any missing data points, aiding in monitoring the script’s accuracy and performance.

## Notes
- Error Handling: The script is designed to handle missing data gracefully, logging any missing information for further inspection.
- Review Extraction: The extraction function ensures only numerical review counts are stored, filtering out any text to preserve data quality.

