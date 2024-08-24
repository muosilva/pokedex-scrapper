import scrapy


class PokedexSpider(scrapy.Spider):
    name = "pokedex"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net"]

    def parse(self, response):
        pass
