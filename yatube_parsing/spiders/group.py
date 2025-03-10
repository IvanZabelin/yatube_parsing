import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        all_groups = response.css('a.group_link::attr(href)')
        for group in all_groups:
            yield response.follow(group, callback=self.parse_group)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    
    def parse_group(self, response):
        yield{
            'group_name': response.css('h2::text').get(),
            'description': response.css('p.group_descr::text').get(default='').strip(),
            'posts_count': int(response.css('div.h6.text-muted.posts_count::text').get(default='').replace('Записей: ', '').strip()),
        }