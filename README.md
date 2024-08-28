# Projeto Pokedex Web Scraping

Este projeto realiza a extração de dados da Pokédex do site [Pokémon Database](https://pokemondb.net/) utilizando Python, Scrapy e Pandas. O objetivo é coletar informações detalhadas sobre os Pokémon e gerar um arquivo JSON contendo os dados.

## Passos para Configuração

1. **Clone o repositório do projeto**:
   ```bash
   git clone https://github.com/muril0-o/pokedex-scrapper.git
    ```
2. **Navegue até a pasta `pokedex`**:
   ```bash
   cd pokedex
   ```
3. **Crie um ambiente virtual**:
   ```bash
   python3 -m venv venv
   ```
4. **Ative o ambiente virtual**:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. **Instale as dependências**:
   - Instale o Scrapy:
     ```bash
     pip install scrapy
     ```
   - Instale o Pandas:
     ```bash
     pip install pandas
     ```
6. **Execute o Scraper**:
   ```bash
   python run_spider.py
   ```
7. **Execute o script de tratamento de dados**:
   ```bash
   python unir.py
   ```

## Resultado

O arquivo `pokedex.json` será gerado com os dados dos Pokémon extraídos e tratados.

## Participantes

- Henrique Marques
- Gabriel Reimberg
- Murilo Oliveira
