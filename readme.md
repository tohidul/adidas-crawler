# Crawling Adidas Website

This project crawl product information from shop.adidas.jp. In this project I particularly crawled
men's wear using the following url

https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops

I have crawled the following information

- product url
- product name
- category
- price
- available sizes
- breadcrumb
- title of description
- general description of the product
- general description itemized
- rating
- number of reviews
- recommend rate
- size structure

## Run the project

The project is written on python. Install scrapy, selenium by using the following command

pip install scrapy

pip install selenium

now open the ~/crawling/adidas/settings.py and add the following

SELENIUM_DRIVER_ARGUMENTS = ["--headless=new", "--window-size=1920,1080"]

to run the project go to ~/crawling/adidas and run the following command

scrapy crawl clothing_selenium -o <output_json_file_path>

this will generate a json file containing crawled data

to convert the json dataset to excel file run the following script

python ~/crawling/convert_crawled_json_to_excel.py <generated_json_file_path> <excel_output_file>


This will generate the desired excel file.


