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

            item["numero"] = numero
            item["link"] = link
            item["nome"] = nome
            item["tipos"] = tipos

            request = scrapy.Request(url=link, callback=self.parse_pokemon)

            request.meta['item'] = item
            
            yield request

            break

    def parse_pokemon(self, response):
        item = response.meta['item']
        
        # Extraindo os detalhes
        altura = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        peso = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()

        evolucoes_id = response.css('div.infocard-list-evo > div.infocard > span.infocard-lg-data > small:nth-child(1)::text').getall()
        evolucoes_nome = response.css('div.infocard-list-evo > div.infocard > span.infocard-lg-data > a::text').getall()
        evolucoes_link = response.css('div.infocard-list-evo > div.infocard > span.infocard-lg-data > a::attr(href)').getall()

        habilidade_nome = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::text').getall()
        habilidade_link = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::attr(href)').getall()
        habilidade_descricao = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::attr(title)').getall()

        evolucoes = []
        habilidades= []
        passou_atual = False

        for i in range(len(evolucoes_id)):
            if (not passou_atual):
                if (evolucoes_id[i][1:] == item["numero"]):
                    passou_atual = True
            #elif (evolucoes_id[i][1:] != item["numero"] and int(evolucoes_id[i][1:]) > int(item["numero"])):
            else:
                evolucao = {
                    "numero": evolucoes_id[i],
                    "nome": evolucoes_nome[i],
                    "link": evolucoes_link[i]
                }
                if evolucao not in evolucoes:
                    evolucoes.append(evolucao)

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
        item['evolucoes'] = evolucoes
        item['habilidades'] = habilidades
        
        yield item

# Tratamentos a serem feitos
# Só deixar os números do Id, peso e altura