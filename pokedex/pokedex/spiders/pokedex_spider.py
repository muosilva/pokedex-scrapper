import scrapy
from ..items import PokedexItem, EvolutionItem, HabilidadeItem

#venv\Scripts\activate
domain = "https://www.pokemondb.net"

class PokedexSpider(scrapy.Spider):
    name = "pokedex_spider"
    start_urls = ["https://pokemondb.net/pokedex/all"]
    file_path = 'pokemon.json'

    def __init__(self):
        with open(self.file_path, 'w') as json_file:
            json_file.write('')

    def parse(self, response):
        pokemon_anterior = 0
        #pokemons = response.css('#pokedex > tbody > tr')

        for pokemon in response.css('#pokedex > tbody > tr'):
            item = PokedexItem()

            item["numero"] = pokemon.css("td.cell-num > span::text").extract_first()
            item["link"] = domain + pokemon.css("td.cell-name > a::attr(href)").extract_first()
            item["nome"] = pokemon.css("td.cell-name > a::text").extract_first()
            item["tipos"] = pokemon.css("td.cell-icon > a::text").getall()

            if (pokemon_anterior == item["numero"]):
                continue

            pokemon_anterior = item["numero"]

            request = scrapy.Request(url=item["link"], callback=self.parse_method)

            request.meta['item'] = item
            
            yield request

    def parse_method(self, response):
        item = response.meta['item']
        
        # Extraindo os detalhes
        item['altura'] = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        item['peso'] = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()

        habilidade_nome = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::text').getall()

        habilidades = []

        for habilidade in habilidade_nome:
            habilidades.append({
                'nome': habilidade
            })
        
        # Adiciona os detalhes ao item
        item['evolucoes'] = []
        item['habilidades'] = habilidades
        
        yield item

class PokedexEvo(scrapy.Spider):
    name = "pokedex_evo"
    start_urls = ["https://pokemondb.net/evolution/"]
    file_path = "pokemon_evo.json"

    def __init__(self):
        with open(self.file_path, 'w') as json_file:
            json_file.write('')

    def parse(self, response):
        tipos_evo = ['level', 'stone', 'trade', 'friendship', 'status']
        for tipo in tipos_evo:
            next_page = f'https://pokemondb.net/evolution/{tipo}'
            yield scrapy.Request(next_page, callback=self.parse_method)

    def parse_method(self, response):
        for evo in response.css('tbody tr'):
            item = EvolutionItem()
            item["pokemon_origem"] = evo.css('td:nth-child(1) a::attr(title)').get()[18:22]
            item["pokemon_destino"] = evo.css('td:nth-child(3) a::attr(title)').get()[18:22]

            yield item

class PokedexHabilidades(scrapy.Spider):
    name = "pokedex_hab"
    start_urls = ["https://pokemondb.net/ability"]
    file_path = "pokemon_hab.json"

    def __init__(self):
        with open(self.file_path, 'w') as json_file:
            json_file.write('')

    def parse(self, response):
        for habilidade in response.css('#abilities > tbody > tr'):
            item = HabilidadeItem()

            item["nome"] = habilidade.css("td:nth-child(1) > a::text").extract_first()
            item["link"] = domain + habilidade.css("td:nth-child(1) > a::attr(href)").extract_first()

            request = scrapy.Request(url=item["link"], callback=self.parse_method)

            request.meta['item'] = item
            
            yield request

    def parse_method(self, response):
        item = response.meta['item']
        
        item['descricao'] = ''.join(response.css('main > div.grid-row > div.grid-col > p ::text').getall())

        yield item