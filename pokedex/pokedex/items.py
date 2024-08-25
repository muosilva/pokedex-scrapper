# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PokedexItem(scrapy.Item):
    # define the fields for your item here like:
    numero = scrapy.Field()
    link = scrapy.Field()
    nome = scrapy.Field()
    tipos = scrapy.Field()
    peso = scrapy.Field()
    altura = scrapy.Field()

    # - Próximas evoluções do Pokémon se houver (Número, nome e URL)
    # - Habilidades (link para outra página)
    #     - URL da página
    #     - Nome
    #     - Descrição do efeito