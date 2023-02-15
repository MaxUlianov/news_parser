import scrapy


class AmurInfoSpider(scrapy.Spider):
    name = "amur_info"
    start_urls = [
        'https://amur.info/category/все-новости/?article-category=1627&articles-date=05%2F02%2F2023+-+15%2F02%2F2023'
    ]

    """
    Использовал hard-coded интервал, но можно задавать через datetime
    (date_interval.py)
    """

    custom_settings = {
        'FEEDS': {'data.csv': {'format': 'csv', }},
        'HTTPERROR_ALLOWED_CODES': [301],
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
    }

    def __init__(self, param='светофор', *args, **kwargs):
        """
        :param param: слово / строка, которую парсер ищет в заголовке
        """
        super().__init__(*args, **kwargs)
        self.param = param

    def parse(self, response):
        search_string = self.param
        xpath = f"//a[@class='h2' and contains(., '{search_string}')]"

        news = response.xpath(xpath)

        for item in news:
            print({
                'text': item.xpath("text()").get(),
                'link': item.xpath("@href").extract()
            })

            yield {
                'link': item.xpath("@href").extract()[0]
            }

        next_page = response.xpath("//a[@class='pagination__nav']/@href").extract()

        """
        Проверка на то, дошел ли парсер до последней страницы
        (из-за переадресации на сайте DupeFilter Scrapy блокирует переход на
        следующую страницу, поэтому приходится его отключать (custom settings) и
        останавливать парсер таким способом)
        """
        current = response.request.url
        last = response.xpath("//a[@class='pagination__link']")[-1].xpath("text()").get()

        if current.find('page/') != -1:
            current_num = current[current.index('page/')+len('page/'):current.index('/?article')]
            if current_num == last:
                return

        if next_page is not None and next_page != []:
            yield response.follow(next_page[-1], callback=self.parse)
