import pandas as pd
import re

def formatar_numero(numero):
    return str(numero).zfill(4)

def converter_altura_peso(valor, tipo):
    match = re.search(r"([\d\.]+)", valor)
    if match:
        valor_convertido = float(match.group(1))
        if tipo == "altura":
            return valor_convertido * 100  # Converte metros para centímetros
        return valor_convertido
    return None

def obter_habilidades(nome_habilidades, habilidades_df):
    habilidades_info = habilidades_df[habilidades_df['nome'].isin(nome_habilidades)].to_dict(orient='records')
    return habilidades_info

def unir_evolucoes():
    poke_df = pd.read_json('pokemon.json', encoding='utf-8')
    evo_df = pd.read_json('pokemon_evo.json', encoding='utf-8')
    hab_df = pd.read_json('pokemon_hab.json', encoding='utf-8')

    hab_df = pd.DataFrame(hab_df)

    poke_dict = poke_df.set_index('numero').to_dict(orient='index')

    def adicionar_evolucoes(row):
        evolucoes = []
        evolucao_para = evo_df[evo_df['pokemon_origem'] == row['numero']]
        
        for _, evo in evolucao_para.iterrows():
            para_numero = evo['pokemon_destino']
            if para_numero in poke_dict:
                evolucao_info = {
                    "numero": formatar_numero(para_numero),
                    "nome": poke_dict[para_numero]["nome"],
                    "link": poke_dict[para_numero]["link"]
                }
                if evolucao_info not in evolucoes:
                    evolucoes.append(evolucao_info)
        
        return evolucoes

    poke_df['evolucoes'] = poke_df.apply(adicionar_evolucoes, axis=1)

    poke_df['numero'] = poke_df['numero'].apply(formatar_numero)
    poke_df['altura'] = poke_df['altura'].apply(lambda x: converter_altura_peso(x, "altura"))
    poke_df['peso'] = poke_df['peso'].apply(lambda x: converter_altura_peso(x, "peso"))

    poke_df['habilidades'] = poke_df['habilidades'].apply(lambda x: obter_habilidades([h['nome'] for h in x], hab_df))

    poke_df.to_json('poke_updated.json', orient='records', indent=4, force_ascii=False)

unir_evolucoes()