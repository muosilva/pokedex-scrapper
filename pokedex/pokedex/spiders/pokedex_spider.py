import scrapy
from ..items import PokedexItem

#venv\Scripts\activate

class PokedexSpider(scrapy.Spider):
    name = "pokedex_spider"
    domain = "https://www.pokemondb.net"
    start_urls = ["https://pokemondb.net/pokedex/all"]
    file_path = 'pokemon.json'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limpa o conteúdo do arquivo JSON no início
        with open(self.file_path, 'w') as json_file:
            json_file.write('')

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

            item["numero"] = numero
            item["link"] = link
            item["nome"] = nome
            item["tipos"] = tipos

            request = scrapy.Request(url=link, callback=self.parse_pokemon)

            request.meta['item'] = item
            
            yield request

    def parse_pokemon(self, response):
        item = response.meta['item']
        
        # Extraindo os detalhes
        altura = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        peso = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()

        habilidade_nome = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::text').getall()
        habilidade_link = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::attr(href)').getall()
        habilidade_descricao = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::attr(title)').getall()

        habilidades = []   

        for i in range(len(habilidade_nome)):
            habilidade = {
                'nome': habilidade_nome[i],
                'link': habilidade_link[i],
                'descricao': habilidade_descricao[i]
            }
            habilidades.append(habilidade)
        
        # Adiciona os detalhes ao item
        item['altura'] = altura
        item['peso'] = peso
        item['evolucoes'] = []
        item['habilidades'] = habilidades
        
        yield item

class PokedexEvo(scrapy.Spider):
    name = "pokedex_evo"
    domain = "https://www.pokemondb.net"
    start_urls = ["https://pokemondb.net/evolution/"]
    file_path = "pokemon_evo.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limpa o conteúdo do arquivo JSON no início
        with open(self.file_path, 'w') as json_file:
            json_file.write('')

    def parse(self, response):
        methods = ['level', 'stone', 'trade', 'friendship', 'status']
        for method in methods:
            next_page = f'https://pokemondb.net/evolution/{method}'
            yield scrapy.Request(next_page, callback=self.parse_method)

    def parse_method(self, response):
        for row in response.css('tbody tr'):
            item = {}
            evolves_from = row.css('td:nth-child(1) a::attr(title)').get()
            evolves_to = row.css('td:nth-child(3) a::attr(title)').get()

            if evolves_from:
                item["de"] = evolves_from.replace('View Pokedex for #', '')[:4]
            if evolves_to:
                item["para"] = evolves_to.replace('View Pokedex for #', '')[:4]

            if item:
                yield item

# Tratamentos a serem feitos
# Só deixar os números do Id, peso e altura