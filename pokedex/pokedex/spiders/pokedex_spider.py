import scrapy
from ..items import PokedexItem

#venv\Scripts\activate

class PokedexSpider(scrapy.Spider):
    name = "pokedex_spider"
    domain = "https://www.pokemondb.net"
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response):
        pokemon_anterior = 0
        pokemons = response.css('#pokedex > tbody > tr')

        for pokemon in pokemons:
            item = PokedexItem()

            numero = pokemon.css("td.cell-num > span::text").extract_first()
            link = self.domain + pokemon.css("td.cell-name > a::attr(href)").extract_first()
            nome = pokemon.css("td.cell-name > a::text").extract_first()
            tipos = pokemon.css("td.cell-icon > a::text").getall()

            if (pokemon_anterior == numero):
                continue

            pokemon_anterior = numero

            item["numero"] = int(numero)
            item["link"] = link
            item["nome"] = nome
            item["tipos"] = tipos

            request = scrapy.Request(url=link, callback=self.parse_pokemon)

            request.meta['item'] = item
            
            yield request

            #break

    def parse_pokemon(self, response):
        item = response.meta['item']
        
        # Extraindo os detalhes
        altura = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        peso = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()
        
        # Adiciona os detalhes ao item
        item['altura'] = altura
        item['peso'] = peso
        
        yield item