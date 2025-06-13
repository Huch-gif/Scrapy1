
import scrapy

class RonaLightsSpider(scrapy.Spider):
    name = "rona_lights"
    allowed_domains = ["rona-servis.ru"]
    start_urls = ["https://www.rona-servis.ru/catalog"]

    def parse(self, response):
        # Шаг 1: Парсим ссылки на категории освещения
        categories = response.css('.collection-preview__link::attr(href)').getall()
        for category in categories:
            yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response):
        # Шаг 2: Парсим товары на странице категории
        products = response.css('.product-preview')
        for product in products:
            yield {
                'name': product.css('.product-preview__description::text').get(),
                'price': product.css('.price-current::text').get(),
                'url': response.urljoin(product.css('a::attr(href)').get())
            }

        # Шаг 3: Переход на следующую страницу (если есть)
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category)