import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import urllib
from heroku_database import get_categories, insert_item, get_items_from_database


def extract_etsy_items(number_of_items: int, category: str) -> pd.DataFrame:
    """
    Scrapes www.etsy.com for requested number of items and search word(s) as
    category.
    :return: items with title, link, price and image link.
    """
    print(f"Scrapping category \"{category}\"")
    result = []
    page_number = 1
    headers = {"User-Agent": "Mozilla/5.0"}

    while len(result) < number_of_items:
        time.sleep(2)
        url = f"https://www.etsy.com/search?q={make_url_compatible(category)}" \
              f"&ref=pagination&page={page_number} "

        source = requests.get(url, headers=headers)
        soup = BeautifulSoup(source.content, "html.parser")

        items = soup.select("li.wt-list-unstyled")
        if len(items) == 0:
            print(f'Total items of {category} was found less than requested: '
                  f'{len(result)}')
            break

        for item in items:
            if len(result) >= number_of_items:
                break

            record = extract_item_data(item)
            if record:
                result.append(record)

        page_number += 1

    return pd.DataFrame(result)


def make_url_compatible(category: str) -> str:
    """Converts string to URL compatible."""
    return urllib.parse.quote(category)


def extract_item_data(item) -> dict:
    """Extract item data: title, link, price and image link."""
    record = {}

    main_tag = item.find("a", class_="listing-link")
    if main_tag:
        record["title"] = main_tag.get("title")
        record["itemURL"] = main_tag.get("href")
    if "title" not in record:
        return None

    price_tag = item.find("span", class_="currency-value")
    if price_tag:
        record['price'] = normalize_price(price_tag.text)

    placeholder_tag = item.find("div", class_="placeholder")
    if placeholder_tag:
        img_tag = placeholder_tag.find("img")
        if img_tag:
            record["imgURL"] = img_tag.get("src")

    return record


def normalize_price(price: str) -> float:
    """Normalizes USD price with thousand separator into float value"""
    return float(price.strip().replace(',', ''))


def get_all_categories_items(number_of_items: int) -> pd.DataFrame:
    """
    Take a list of categories from categories table in database.
    Scrapes website for all of them.
    Prepare data for inserting to the database.
    :return: All items scrapped.
    """
    all_items = pd.DataFrame()
    for (category_id, category_name) in get_categories():
        items = extract_etsy_items(number_of_items, category_name)
        items['categoryId'] = category_id
        items = items[['categoryId', 'title', 'price', 'itemURL', 'imgURL']]
        items.set_index('categoryId', inplace=True)
        all_items = all_items.append(items)
    return all_items


def save_items_to_database(items: pd.DataFrame) -> None:
    """Insert all items into the database."""
    for item in items.itertuples():
        insert_item(item)


def save_items_to_csv(items_data: pd.DataFrame):
    """Exports given file to csv."""
    with open('etsy_items.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(items_data)


all_category_items = get_all_categories_items(3000)
save_items_to_database(all_category_items)

data = get_items_from_database()
save_items_to_csv(data)
