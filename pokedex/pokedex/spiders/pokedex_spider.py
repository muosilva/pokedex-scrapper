import scrapy
from scrapy.selector import Selector
from ..items import PokedexItem
#import json

#venv\Scripts\activate

class PokedexSpider(scrapy.Spider):
    name = "pokedex_spider"
    domain = "https://www.pokemondb.net"
    start_urls = ["https://pokemondb.net/pokedex/all"]
    file_path = 'pokemon.json'

    # retirar isso
    var_qualquer = 0

    # Função para limpar o JSON
    with open(file_path, 'w') as json_file:
        pass

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

            self.var_qualquer += 1
            if self.var_qualquer >= 1:
                break

    def parse_pokemon(self, response):
        item = response.meta['item']
        
        # Extraindo os detalhes
        altura = response.css('.vitals-table > tbody > tr:nth-child(4) > td::text').get()
        peso = response.css('.vitals-table > tbody > tr:nth-child(5) > td::text').get()

        #evolucoes_element = response.css('div.infocard-list-evo > div.infocard > span.infocard-lg-data')
        #evolucao_elements = response.css('div.infocard-list-evo > div.infocard')
        #evolucao_split = response.css('span.infocard-evo-split')

        #evolucoes_id = response.css('div.infocard-list-evo > div.infocard > span.infocard-lg-data > small:nth-child(1)::text').getall()
        #evolucoes_nome = response.css('div.infocard-list-evo > div.infocard > span.infocard-lg-data > a::text').getall()
        #evolucoes_link = response.css('div.infocard-list-evo > div.infocard > span.infocard-lg-data > a::attr(href)').getall()

        habilidade_nome = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::text').getall()
        habilidade_link = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::attr(href)').getall()
        habilidade_descricao = response.css('div.grid-row > div.grid-col:nth-child(2) > table > tbody > tr:nth-child(6) > td > .text-muted > a::attr(title)').getall()

        habilidades = []
        evolucoes = []

        #for i in range(len(evolucoes_id)):
        #    if (not passou_atual):
        #        if (evolucoes_id[i][1:] == item["numero"]):
        #            passou_atual = True
        #    elif (len(evolucoes_element[i].css("small")) == 2):
        #        if bool(evolucao_split.css(evolucao_elements)):
        #            evolucao = {
        #                "numero": evolucoes_id[i],
        #                "nome": evolucoes_nome[i],
        #                "link": evolucoes_link[i]
        #            }
        #            if evolucao not in evolucoes:
        #                evolucoes.append(evolucao)

        evolucoes_div_geral = response.css('main > div.infocard-list-evo')
        evolucoes_div = evolucoes_div_geral.css('div.infocard')
        evolucoes_span = evolucoes_div_geral.css('span')
        evolucoes_class = evolucoes_span.css('::attr(class)').getall()

        class_evolucao_direta = "infocard-arrow"
        class_evolucao_split = "infocard-list-evo"

        passou_atual = False
        evolucoes = []

        # Itera sobre as classes para identificar evoluções
        for i in range(len(evolucoes_class)):
            evolucao_info = None
            
            # Verifica se é uma evolução split
            if class_evolucao_split in evolucoes_class[i]:
                if i + 1 < len(evolucoes_span):
                    evolucao_info = evolucoes_span[i + 1]
            # Verifica se é uma evolução direta
            elif class_evolucao_direta in evolucoes_class[i]:
                if i + 1 < len(evolucoes_div):
                    evolucao_info = evolucoes_div[i + 1]
            
            if evolucao_info:
                evolucao_id = evolucao_info.css('span.infocard-lg-data > small:nth-child(1)::text').get()
                evolucao_nome = evolucao_info.css('span.infocard-lg-data > a::text').get()
                evolucao_link = evolucao_info.css('span.infocard-lg-data > a::attr(href)').get()

                if evolucao_id:
                    if not passou_atual:
                        # Verifica se o Pokémon atual é o base, se sim, ignora
                        if evolucao_id[1:] == item["numero"]:
                            passou_atual = True
                    else:
                        # Adiciona a evolução à lista de evoluções
                        evolucao = {
                            "numero": evolucao_id,
                            "nome": evolucao_nome,
                            "link": evolucao_link
                        }
                        if evolucao not in evolucoes:
                            evolucoes.append(evolucao)
                        # Se for uma evolução direta, paramos de procurar
                        if class_evolucao_direta in evolucoes_class[i]:
                            break


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
# Se id 841 ou 842 não tem evolução
# Incluir { "numero": 0413, "nome": Wormadam, "link": /pokedex/wormadam } ao #0411