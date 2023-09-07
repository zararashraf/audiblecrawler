import scrapy

class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def parse(self, response):

        container = response.css('div.adbl-impression-container')
        products = container.xpath('.//li[contains(@class, "productListItem")]')

        for product in products:
            heading = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').get()
            price = product.xpath('.//p[contains(@class, "buybox-regular-price")]/span[2]/text()').get().strip()
            length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()[9:]

            yield {
                'heading': heading,
                'author': author,
                'price': price,
                'length': length
            }

        pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
        next_page_url = pagination.xpath('.//span[contains(@class, "nextButton")]/a/@href').get()

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)