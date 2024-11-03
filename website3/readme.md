# E-commerce Web Scraping Project

## Overview
A robust web scraping solution designed to extract product information from e-commerce websites using Selenium and BeautifulSoup. The project handles dynamic AJAX-loaded content and implements comprehensive logging for monitoring and debugging.

## Key Features
- Dynamic content handling with Selenium WebDriver
- Automated pagination navigation
- Structured data extraction for product details
- Comprehensive logging system
- Error handling and recovery mechanisms
- Data export to CSV format

## Prerequisites
- Python 3.7+
- Chrome WebDriver
- Git (for version control)

## Required Dependencies
```bash
pip install -r requirements.txt
```

Key packages:
- selenium==4.26.1
- beautifulsoup4==4.12.3
- pandas==2.2.3
- requests==2.32.3


## Project Structure
```
Webscraping Project/
├── website1/
│   ├── scrap.py
│   └── data/
│       └── data_[timestamp].csv
├── website2/
│   ├── scrap.py
│   └── data/
│       └── data_[timestamp].csv
├── website3/
│   ├── scrap.py
│   ├── web_scrap_log.txt
│   └── data/
│       └── data_[timestamp].csv
├── README.md
└── requirements.txt
```

## Configuration
Before running the script, update the following variables in `scrap.py`:

```python
home_dir = "/path/to/your/project/"
driver_dir = '/path/to/your/chromedriver'
```

## Features

### Data Extraction
The script extracts the following product information:
- Product name
- Price
- Description
- Rating (0-5 stars)
- Review count

### Pagination Handling
- Automated navigation through product pages
- Configurable maximum page limit
- Wait conditions for AJAX content loading

### Logging System
- Detailed timestamped logs
- Operation tracking for:
  - Page navigation
  - Data extraction
  - Error occurrences
  - Processing completion

## Usage

1. Clone the repository:
```bash
git clone https://github.com/Chideraozigbo/WebScrapeChallenge.git
cd Webscraping\ Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scraper:
```bash
python website3/scrap.py
```

## Output
- Extracted data is saved in CSV format: `data_YYYY-MM-DD_HH-MM-SS.csv`
- Log file: `web_scrap_log.txt`

## Error Handling
The script implements robust error handling for:
- Network connectivity issues
- Missing webpage elements
- Data extraction failures
- Pagination navigation errors

## Logging Details
Log entries include:
- Timestamp for each operation
- Page navigation status
- Data extraction progress
- Error messages and stack traces
- Processing completion status

## Performance Considerations
- Implements wait times to respect website resources
- Uses explicit waits for dynamic content
- Efficiently handles memory usage during large data extractions

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request



## Troubleshooting
Common issues and solutions:

### WebDriver Issues
- Ensure Chrome WebDriver version matches your Chrome browser version
- Verify WebDriver path is correctly set in the script
- Check system PATH includes WebDriver location

### Data Extraction Problems
- Verify website structure hasn't changed
- Check network connectivity
- Review logs for specific error messages

## Future Improvements
- [ ] Add proxy support
- [ ] Implement concurrent scraping
- [ ] Add database storage option
- [ ] Create API endpoint for data access
- [ ] Add support for additional e-commerce platforms

## Support
For issues and feature requests, please create an issue in the GitHub repository.