import scrapy


class AmurInfoSpider(scrapy.Spider):
    name = "amur_info"

    start_urls = [
        'https://amur.info/category/все-новости/?article-category=1627&articles-date=05%2F02%2F2023+-+15%2F02%2F2023'
    ]

    def parse(self, response):
        search_string = 'суд'
        xpath = f"//a[@class='h2' and contains(., '{search_string}')]"

        news = response.xpath(xpath)

        # for item in news:
        #     print(item.xpath("text()").get())
        #     print(item.xpath("@href").extract())

        for item in news:
            yield {
                'text': item.xpath("text()").get(),
                'link': item.xpath("@href").extract()
            }

        next_page = response.xpath("//a[@class='pagination__nav']/@href").extract()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
