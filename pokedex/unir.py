import pandas as pd
import re

def formatar_numero(numero):
    return str(numero).zfill(4)  # Preencher com zeros à esquerda para garantir 4 dígitos

def converter_altura_peso(valor):
    # Extrair apenas o número e converter para float
    match = re.search(r"([\d\.]+)", valor)
    if match:
        return float(match.group(1))
    return None

def unir_evolucoes():
    # Ler os dados dos arquivos JSON
    poke_df = pd.read_json('pokemon.json')
    evo_df = pd.read_json('pokemon_evo.json')

    # Transformar o DataFrame em dicionário com o número como chave
    poke_dict = poke_df.set_index('numero').to_dict(orient='index')

    def adicionar_evolucoes(row):
        evolucoes = []
        evolucao_para = evo_df[evo_df['de'] == row['numero']]
        
        for _, evo in evolucao_para.iterrows():
            para_numero = evo['para']
            if para_numero in poke_dict:
                evolucao_info = {
                    "numero": formatar_numero(para_numero),
                    "nome": poke_dict[para_numero]["nome"],
                    "link": poke_dict[para_numero]["link"]
                }
                if evolucao_info not in evolucoes:
                    evolucoes.append(evolucao_info)
        
        return evolucoes

    # Aplicar a função para adicionar evoluções sem duplicatas
    poke_df['evolucoes'] = poke_df.apply(adicionar_evolucoes, axis=1)

    # Formatar o número, altura e peso
    poke_df['numero'] = poke_df['numero'].apply(formatar_numero)
    poke_df['altura'] = poke_df['altura'].apply(converter_altura_peso)
    poke_df['peso'] = poke_df['peso'].apply(converter_altura_peso)

    # Salvar o DataFrame atualizado em um novo arquivo JSON
    poke_df.to_json('poke_updated.json', orient='records', indent=4)

# Chamar a função de união ao final dos spiders
unir_evolucoes()
