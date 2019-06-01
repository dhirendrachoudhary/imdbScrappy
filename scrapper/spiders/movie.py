from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#import scrapy

SEARCH_QUERY = (
    'https://www.imdb.com/search/title?'
    'title_type=feature&'
    'user_rating=1.0,10.0&'
    'countries=us&'
    'languages=en&'
    'count=250&'
    'view=simple'
)

class MovieSpider(CrawlSpider):
    name = 'movie'
    allowed_domains = ['imdb.com']
    start_urls = [
        SEARCH_QUERY
        ]

    rules = (Rule(
        LinkExtractor(restrict_css=('div.desc a')),
        follow=True,
        callback='parse_query_page',
    ),)

    def parse_query_page(self, response):
        links = response.css('span.lister-item-header a::attr(href)').extract()
        for link in links:
           yield response.follow(link, callback=self.parse_movie_detail_page)

    def parse_movie_detail_page(self, response):
        data = {}
        data['title'] = response.css('h1::text').extract_first().strip()
        data['year'] = response.css('#titleYear a::text').extract_first()
        data['users_rating'] = response.xpath('//span[contains(@itemprop, "ratingValue")]/text()').extract_first()
        data['imdb_url'] = response.url.replace('?ref_=adv_li_tt', '')

        yield data
