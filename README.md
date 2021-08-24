# SQL and Data Scraping

* Creating database structure with PostgreSQL, hosted on Heroku. Communicating with database with psycopg2  
* Data scrapping with Beautiful Soup for 3 categories, 3000 items each, on www.etsy.com
* Pushing the data to database and exporting to csv

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Launching site scraping](#launching-site-scraping)
* [Features](#features)
* [Status](#status)
* [License](#license)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
Database creation and data scrapping was done for learning purposes.  
Project contains two Python files: one with database specifics, another for site scrapping.  

While scrapping the site, many items were returned empty. My guess is that it's because of the JavaScript loading the products. Additional 
code lines were included to avoid it.  
Applied price normalization in order to be able to convert values into floats. 

## Technologies
* Python - version 3.8
* beautifulsoup4 - version 4.9.3
* psycopg2-binary - version 2.8.6   
   
_for more please read requirements.txt_

## Setup
- Create a PostgreSQL database on Heroku
- Add database credentials to .env file (you can use .env.example as a reference) 
- Run `pip install -r requirements.txt` to install project requirements
- Run `python heroku_database.py` to create a database structure and add initial categories 

## Launching site scraping
Run `python site_scraping.py` in order to pull 3000 items from each category (defined in _categories_ table) into database and export into csv file

## Features: 
* Scrape any category on www.etsy.com, as many items as you want (if quantity is available on site)
* Push data to PostgreSQL database
* Extract data from database
* Export data to csv

## Status
Project is: _finished_

## License
>You can check out the full license [here](https://opensource.org/licenses/MIT)

This project is licensed under the terms of the **MIT** license.

## Inspiration
Learning @Turing College

## Contact
Created by [Juste Gaviene](mailto:juste.gaviene@gmail.com?subject=[GitHub]%20Source%20Han%20Sans)
