import scrapy

class RonaLightsSpider(scrapy.Spider):
    name = "rona_lights"
    allowed_domains = ["rona-servis.ru"]
    start_urls = ["https://rona-servis.ru/catalog/svet/"]

    def parse(self, response):
        for product in response.css('div.product-item'):
            yield {
                'name': product.css('a::text').get().strip(),
                'price': product.css('span.price::text').get().replace(' ', ''),
                'url': response.urljoin(product.css('a::attr(href)').get())
            }