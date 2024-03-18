import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import time

class ClothingSpiderSelenium(scrapy.Spider):
    name = "clothing_selenium"
    allowed_domains = ["shop.adidas.jp"]
    start_urls = ["https://shop.adidas.jp"]

    def parse(self, response):
        driver = webdriver.Firefox()
        driver.set_window_size(1920, 1080)
        total_page = 10
        p = 0
        scroll_pause_time = 1
        screen_height = driver.execute_script("return window.screen.height;")
        while p < total_page:
            driver.get(r"https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&page={}".format(p))
            i = 1
            while True:
                driver.execute_script(
                    "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                i += 1
                time.sleep(scroll_pause_time)
                scroll_height = driver.execute_script("return document.body.scrollHeight;")
                if (screen_height) * i > scroll_height:
                    break
            self.html = driver.page_source
            p = p + 1
            resp = Selector(text=self.html)

            for product_path in resp.xpath(r"//div[@class='articleDisplayCard-children']/a/@href").extract():
                    product_url = self.start_urls[0]+product_path
                    driver.get(product_url)
                    j=1
                    while True:
                        driver.execute_script(
                            "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=j))
                        j += 1
                        time.sleep(scroll_pause_time)
                        scroll_height = driver.execute_script("return document.body.scrollHeight;")
                        if (screen_height) * j > scroll_height:
                            break
                    self.html_inner = driver.page_source
                    resp_inner = Selector(text=self.html_inner)
                    yield {
                        'product_url': product_url,
                        'product_name': resp_inner.xpath("//h1[@class='itemTitle test-itemTitle']/text()").get(),
                        'category': resp_inner.xpath("//span[@class='genderName test-genderName']/text()").get(),
                        'price': resp_inner.xpath(
                            "//div[contains(@class, 'articlePrice')]/p[contains(@class, 'price-text test-price-text')]/span[contains(@class, 'price-value')]/text()").get(),
                        'available_size': resp_inner.xpath(
                            "//button[contains(@class,'sizeSelectorListItemButton') and not(contains(@class,'disable'))]/text()").getall(),
                        'breadcrumb': resp_inner.xpath(
                            "//li[contains(@class,'breadcrumb') and not(contains(@class, 'back'))]/a/text()").getall(),
                        "title_of_description": resp_inner.xpath("//h4[contains(@class,'heading')]/text()").get(),
                        "general_description_of_the_product": resp_inner.xpath(
                            "//div[contains(@class,'commentItem-mainText')]/text()").get(),
                        "general_description_itemized": resp_inner.xpath(
                            "//li[contains(@class,'articleFeaturesItem')]/text()").getall(),
                        "rating":resp_inner.xpath("//div[@id='BVRRRatingOverall_']//span[@class='BVRRNumber BVRRRatingNumber']/text()").get(),
                        "number_of_reviews": resp_inner.xpath(
                            "//span[@class='BVRRNumber BVRRBuyAgainTotal']/text()").get(),
                        "recommend_rate": resp_inner.xpath(
                            "//span[@class='BVRRBuyAgainPercentage']/span/text()").get(),
                        "size_header": resp_inner.xpath(
                            "//th[@class='sizeChartTHeaderCell test-combined_table_header']/text()").getall(),
                        "size_chart": resp_inner.xpath("//td[@class='sizeChartTCell']/span/text()").getall()

                    }

