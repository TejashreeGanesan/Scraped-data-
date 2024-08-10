# Goodreads Book Data Scraper

## Overview

This project is a web scraper built with Scrapy to extract book data from Goodreads. 
It collects detailed information about books from various genres and categories, such as "New Releases" and "Most Read Recently." 
The data includes book names, authors, ratings, reviews, and more. The results are saved in an Excel file for easy analysis and review.

## Features

- Scrapes book information from Goodreads.
- Filters and follows links for various genres and categories.
- Collects book details such as name, author, rating stars, number of reviews, and more.
- Exports the data to an Excel file.

## Installation

### Clone the repository:

> git clone repository-url

> cd repository-directory

### Install dependencies:

Ensure you have Python and pip installed. Then, install the required libraries. Here we require scrapy and pandas to be installed, so use the below command to install the libraries

> pip install scrapy pandas

## Code Explanation
- **BookDataScrapedSpider:** The main spider class that handles the scraping process.
  
- **start_urls:** Contains the initial URL to start the scraping.
  
- **parse():** Filters genre links and follows them.
  
- **parse_links():** Handles links for new releases and most-read categories.

- **parse_category_links():** Extracts book links from category pages.

- **parse_book_data():** Scrapes detailed information about each book.

- **closed():** Saves the scraped data to an Excel file when the spider completes.

## Usage

### Running the Scrapy Spider
- To run the Scrapy spider, follow these steps:

- Open a terminal or command prompt.

- Navigate to the project directory where your Scrapy spider file (book_data_scraped_spider.py) is located.
  
> cd path/to/your/project

- Execute the spider using Scrapy. The following command runs the spider defined in book_data_scraped_spider.py:

> scrapy runspider book_data_scraped_spider.py

This command will start the scraping process, where the spider will visit the Goodreads website, follow links to various genres and categories, and extract book information.


