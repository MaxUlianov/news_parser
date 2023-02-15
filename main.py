from scrapy.crawler import CrawlerProcess
from amur_info_parser.amur_info_parser.spiders.amur_info_spider import AmurInfoSpider


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(AmurInfoSpider)
    process.start()
