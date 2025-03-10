import scrapy

from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        for card in response.css('div.card-body'):
            text = ' '.join(
                line.strip() 
                for line in card.css('p::text').getall() 
                if line.strip()
            )
            if text:
                data = {
                    'author': card.css('strong::text').get(),
                    'text': text,
                    'date': card.css('small.text-muted::text').get()
                }
                yield YatubeParsingItem(data)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
