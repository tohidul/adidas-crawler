import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from shutil import which
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.common.by import By
class ClothingSpiderSelenium(scrapy.Spider):
    name = "clothing_selenium"
    allowed_domains = ["shop.adidas.jp"]
    start_urls = ["https://shop.adidas.jp"]

    # def __init__(self):
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_path = which("chromedriver")
    #     driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    #     driver.get(self.start_urls[0])
    #
    #     rur_tab = driver.find


    def start_requests(self):
        url = "https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops"
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=3)
    def parse(self, response):
        for product_path in response.xpath(r"//div[@class='articleDisplayCard-children']/a/@href").extract():
            product_url = self.start_urls[0]+product_path
            yield response.follow(url=product_url, callback=self.parse_product)
        for i in range(2, 3):
            new_page_url = r"https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&page={}".format(i)

            yield SeleniumRequest(url=new_page_url,
                                callback=self.parse, wait_time=3)
    def parse_product(self, response):
        yield {
            'product_name': response.xpath("//h1[@class='itemTitle test-itemTitle']/text()").get(),
            'category': response.xpath("//span[@class='genderName test-genderName']/text()").get(),
            'price': response.xpath(
                "//div[contains(@class, 'articlePrice')]/p[contains(@class, 'price-text test-price-text')]/span[contains(@class, 'price-value')]/text()").get(),
            'available_size': response.xpath(
                "//button[contains(@class,'sizeSelectorListItemButton') and not(contains(@class,'disable'))]/text()").getall(),
            'breadcrumb': response.xpath(
                "//li[contains(@class,'breadcrumb') and not(contains(@class, 'back'))]/a/text()").getall(),
            "title_of_description": response.xpath("//h4[contains(@class,'heading')]/text()").get(),
            "general_description_of_the_product": response.xpath(
                "//div[contains(@class,'commentItem-mainText')]/text()").get(),
            "general_description_itemized": response.xpath(
                "//li[contains(@class,'articleFeaturesItem')]/text()").getall(),
            "size": response.xpath("//th[@class='sizeChartTHeaderCell test-combined_table_header']/text()").getall(),


        }
        # print(response.body)
