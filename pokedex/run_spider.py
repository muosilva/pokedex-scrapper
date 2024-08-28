import os
from multiprocessing import Process

def run_spider(spider_name, output_file):
    os.system(f"scrapy crawl {spider_name} -o {output_file}")

if __name__ == '__main__':
    spiders = [
        {"name": "pokedex_spider", "output": "pokemon.json"},
        {"name": "pokedex_evo", "output": "pokemon_evo.json"},
        {"name": "pokedex_hab", "output": "pokemon_hab.json"}
    ]

    processes = []

    for spider in spiders:
        process = Process(target=run_spider, args=(spider["name"], spider["output"]))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()