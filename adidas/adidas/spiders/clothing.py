import scrapy
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
class ClothingSpider(scrapy.Spider):
    name = "clothing"
    allowed_domains = ["shop.adidas.jp"]
    start_urls = ["https://shop.adidas.jp"]
    script = '''
        function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc("function() { return document.body.scrollHeight; }")

    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end

    return splash:html()
end
    '''

    def start_requests(self):
        url = "https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops"
        yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'wait':2,'lua_source': self.script, "timeout":10000})
    def parse(self, response):
        for product_path in response.xpath(r"//div[@class='articleDisplayCard-children']/a/@href").extract():
            product_url = self.start_urls[0]+product_path
            yield response.follow(url=product_url, callback=self.parse_product)
        for i in range(2, 3):
            new_page_url = r"https://shop.adidas.jp/item/?gender=mens&category=wear&group=tops&page={}".format(i)

            yield SplashRequest(url=new_page_url,
                                callback=self.parse, endpoint='execute',
                                args={'lua_source': self.script, 'wait': 2})
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
