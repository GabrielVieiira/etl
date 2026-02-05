import pandas as pd
import numpy as np
import json
from typing import Any, List
from etl.schemas import Ponto
from typing import Callable

colunas_horas = [
    "h_diver_abonada",
    "h_normais",
    "desconto",
    "h_noturna",
    "h_extra",
    "h_extra_feriado",
    "extra_sab",
    "extra_dom",
    "extra_semana",
    "h_horas_sumula60",
    "extra_noturna_sab",
    "extra_feriado",
    "extra_noturna_feriado",
    "extra_noturna_dom",
    "extra_noturna_semana",
    "previsto",
    "desconto_abonado",
    "horas_abonada",
    "atraso",
    "saida_antecipada",
    "h_extra_noturna",
    "interjornada",
    "intervalo_a_menor",
    "extra_normal",
    "extra_excessiva",
    "soma_atrasos",
    "extrap50",
    "extrap100",
    "h_jornada",
    "total_calculado",
    "tempo_excedido_refeicao",
    "entrada_antecipada",
    "horas_apos_saida",
    "adicional_noturno_real",
    "noturna_menos_ad_noturno_real",
    "h_diurna",
    "qtd_abono_parcial"
]

colunas_que_vao_do_jeito_que_ta = [
    'codigo','cod_pessoa','data','cod_unidade','cod_centro_custo','nro_semana',
    'nro_semana_ano','cod_empresa','cod_cargo','aceito','nro_dia_semana','dia_semana',
    'situ_original','situacao','justificativa','cod_justificativa_ponto','qtd_abono_total',
    'qtd_abono_parcial','marcacao1', 'latitude_marcacao_1', 'longitude_marcacao_1',
    'marcacao2', 'latitude_marcacao_2', 'longitude_marcacao_2',
    'marcacao3', 'latitude_marcacao_3', 'longitude_marcacao_3',
    'marcacao4', 'latitude_marcacao_4', 'longitude_marcacao_4',
    'marcacao5', 'latitude_marcacao_5', 'longitude_marcacao_5',
    'marcacao6', 'latitude_marcacao_6', 'longitude_marcacao_6',
    'marcacao7', 'latitude_marcacao_7', 'longitude_marcacao_7',
    'marcacao8', 'latitude_marcacao_8', 'longitude_marcacao_8',
    'marcacao9', 'latitude_marcacao_9', 'longitude_marcacao_9',
    'marcacao10', 'latitude_marcacao_10', 'longitude_marcacao_10',
    'marcacao11', 'latitude_marcacao_11', 'longitude_marcacao_11',
    'marcacao12', 'latitude_marcacao_12', 'longitude_marcacao_12',
    'marcacao1_alterada','marcacao2_alterada','marcacao3_alterada','marcacao4_alterada',
    'marcacao5_alterada','marcacao6_alterada','marcacao7_alterada','marcacao8_alterada',
    'marcacao9_alterada','marcacao10_alterada','marcacao11_alterada','marcacao12_alterada',
    'obs_marcacao_alterada','dias_folga_trabalhada','qtd_dias_uteis','maximo_marcacoes_dia',
    'hrentrada','hrini_intervalo','hrfim_intervalo','hrsaida','ultima_marcacao','pos_ultima_marcacao',
]

''' Função para transformar colunas de horas em minutos'''
def _to_minutes(valor: str | int | float | None) -> int | None:
    if pd.isna(valor):
        return None
        
    if isinstance(valor, (int, float)):
        return int(round(valor * 60))
    
    else:
        v = valor.strip()
        if not v:
            return None
        if ':' in v:  # HH:MM ou HH:MM:SS
            parts = [int(p) for p in v.split(':')]
            if len(parts) == 2:
                h, m = parts; s = 0
            else:
                h, m, s = parts[0], parts[1], parts[2]
            return int(round(h*60 + m + s/60))
        # pode vir "8.5" como string
        try:
            return int(round(float(v) * 60))
        except ValueError:
            return None

def transformar_em_minutos(df:pd.DataFrame, colunas:list[str]) -> pd.DataFrame:
    for coluna in colunas:
        df[coluna] = df[coluna].apply(_to_minutes) #type: ignore
    return df

'''Função que renomeia e ordena as colunas do DataFrame criado atraves da requisiçãoconforme a estrutura do banco SQLite.'''
def padronizar_colunas_ponto(df_pontos: pd.DataFrame) -> pd.DataFrame:
    """Renomeia e ordena as colunas do DataFrame conforme a estrutura do banco SQLite."""
    # --- 1️⃣ Mapeamento de colunas: Requisição → Banco ---
    mapa_colunas = {
        'codigo': 'codigo',
        'cod_pessoa': 'cod_pessoa',
        'data': 'data',
        'cod_unidade': 'cod_departamento',
        'cod_centro_custo': 'cod_regional',
        'nro_semana': 'nro_semana',
        'nro_semana_ano': 'nro_semana_ano',
        'cod_empresa': 'cod_empresa',
        'cod_cargo': 'cod_cargo',
        'aceito': 'aceito',
        'ndia_semana': 'dia_semana',
        'dia_semana': 'nro_dia_semana',
        'situ_original': 'situ_original',
        'situacao': 'situacao',
        'justificativa': 'justificativa',
        'cod_justificativa_ponto': 'cod_justificativa_ponto',
        'qtd_abono_total': 'qtd_abono_total',
        'qtd_abono_parcial': 'qtd_abono_parcial',
        'h_diver_abonada': 'min_diver_abonada',
        'h_normais': 'min_normais',
        'desconto': 'min_faltantes',
        'h_noturna': 'min_noturna',
        'h_extra': 'min_extra',
        'h_extra_feriado': 'min_extra_feriado',
        'extra_sab': 'extra_sab',
        'extra_dom': 'extra_dom',
        'extra_semana': 'extra_semana',
        'h_horas_sumula60': 'min_horas_sumula60',
        'extra_noturna_sab': 'extra_noturna_sab',
        'extra_feriado': 'extra_feriado',
        'extra_noturna_feriado': 'extra_noturna_feriado',
        'extra_noturna_dom': 'extra_noturna_dom',
        'extra_noturna_semana': 'extra_noturna_semana',
        'previsto': 'previsto',
        'desconto_abonado': 'desconto_abonado',
        'horas_abonada': 'minutos_abonados',
        'atraso': 'atraso',
        'saida_antecipada': 'saida_antecipada',
        'h_extra_noturna': 'min_extra_noturna',
        'interjornada': 'interjornada',
        'intervalo_a_menor': 'intervalo_a_menor',
        'extra_normal': 'extra_normal',
        'extra_excessiva': 'extra_excessiva',
        'soma_atrasos': 'soma_atrasos',
        'extrap50': 'extrap50',
        'extrap100': 'extrap100',
        'dias_folga_trabalhada': 'dias_folga_trabalhada',
        'qtd_dias_uteis': 'qtd_dias_uteis',
        'maximo_marcacoes_dia': 'maximo_marcacoes_dia',
        'hrentrada': 'hrentrada',
        'hrini_intervalo': 'hrini_intervalo',
        'hrfim_intervalo': 'hrfim_intervalo',
        'hrsaida': 'hrsaida',
        'ultima_marcacao': 'ultima_marcacao',
        'pos_ultima_marcacao': 'pos_ultima_marcacao',
        'h_jornada': 'min_jornada',
        'total_calculado': 'total_calculado',
        'tempo_excedido_refeicao': 'tempo_excedido_refeicao',
        'entrada_antecipada': 'entrada_antecipada',
        'horas_apos_saida': 'min_apos_saida',
        'adicional_noturno_real': 'adicional_noturno_real',
        'noturna_menos_ad_noturno_real': 'noturna_menos_ad_noturno_real',
        'h_diurna': 'minutos_diurnos'
    }

    # --- 2️⃣ Renomeia conforme o mapeamento ---
    df_pontos = df_pontos.rename(columns=mapa_colunas)

    # --- 3️⃣ Define a ordem correta das colunas ---
    ordem_colunas = [
        'codigo', 'cod_pessoa', 'data', 'cod_departamento', 'cod_regional',
        'nro_semana', 'nro_semana_ano', 'cod_empresa', 'cod_cargo',
        'aceito', 'dia_semana', 'nro_dia_semana', 'situ_original', 'situacao',
        'justificativa', 'cod_justificativa_ponto', 'qtd_abono_total', 'qtd_abono_parcial',
        'min_diver_abonada', 'min_normais', 'min_faltantes', 'min_noturna', 'min_extra',
        'min_extra_feriado', 'extra_sab', 'extra_dom', 'extra_semana', 'min_horas_sumula60',
        'extra_noturna_sab', 'extra_feriado', 'extra_noturna_feriado', 'extra_noturna_dom',
        'extra_noturna_semana'
    ]

    # adiciona marcações com latitude e longitude na ordem correta
    for n in range(1, 13):
        ordem_colunas += [
            f'marcacao{n}',
            f'latitude_marcacao_{n}',
            f'longitude_marcacao_{n}'
        ]

    # adiciona o restante das colunas
    ordem_colunas += [
        'marcacao1_alterada','marcacao2_alterada','marcacao3_alterada','marcacao4_alterada',
        'marcacao5_alterada','marcacao6_alterada','marcacao7_alterada','marcacao8_alterada',
        'marcacao9_alterada','marcacao10_alterada','marcacao11_alterada','marcacao12_alterada',
        'obs_marcacao_alterada','previsto','desconto_abonado','minutos_abonados','atraso',
        'saida_antecipada','min_extra_noturna','interjornada','intervalo_a_menor','extra_normal',
        'extra_excessiva','soma_atrasos','extrap50','extrap100','dias_folga_trabalhada',
        'qtd_dias_uteis','maximo_marcacoes_dia','hrentrada','hrini_intervalo','hrfim_intervalo',
        'hrsaida','ultima_marcacao','pos_ultima_marcacao','min_jornada','total_calculado',
        'tempo_excedido_refeicao','entrada_antecipada','min_apos_saida','adicional_noturno_real',
        'noturna_menos_ad_noturno_real','minutos_diurnos'
    ]

    # --- 4️⃣ Reordena apenas colunas existentes ---
    df_pontos = df_pontos[[c for c in ordem_colunas if c in df_pontos.columns]]

    return df_pontos

'''Função para inserir a lontitude e latitude das marcações de ponto'''
def _to_dict(x: str |dict[str,str] | None) -> dict[str, str] | None:
    """Garante dict: aceita dict, JSON em string ou retorna None."""
    if isinstance(x, dict):
        return x
    if isinstance(x, str) and x.strip():
        try:
            return json.loads(x)
        except Exception:
            return None
    return None

def extrair_campo_json(chave: str) -> Callable[[dict[str, object] | None], float]:
    """Gera função que extrai uma chave de um dicionário, ou retorna np.nan."""
    def extrator(d: dict[str, object] | None) -> float:
        if isinstance(d, dict):
            val = d.get(chave)
            return float(val) if isinstance(val, (str)) else np.nan
        return np.nan
    return extrator

def preencher_latlong_marcacoes(df: pd.DataFrame, max_n: int = 12) -> pd.DataFrame:
    for n in range(1, max_n + 1):
        col_marc = f'marcacao{n}'
        col_json = f'json_marcacao{n}'
        lat_col  = f'latitude_marcacao_{n}'
        lon_col  = f'longitude_marcacao_{n}'

        # garante colunas existentes
        if col_marc not in df.columns: df[col_marc] = pd.NaT
        if col_json not in df.columns: df[col_json] = None

        # normaliza json para dict
        sjson = df[col_json].map(_to_dict)

        # há marcação? (não nulo/nem string vazia)
        mask_marc = df[col_marc].astype(str).str.strip().ne('') & df[col_marc].notna()

        df[lat_col] = np.where(
            mask_marc,
            sjson.map(extrair_campo_json('latitude')),
            np.nan
        )

        df[lon_col] = np.where(
            mask_marc,
            sjson.map(extrair_campo_json('longitude')),
            np.nan
        )
    return df

def transform_pontos(raw_data:List[dict[str,Any]]) -> List[Ponto]:
    df = pd.DataFrame(raw_data)
    df = preencher_latlong_marcacoes(df,max_n=12)
    cols_int = [c for c in colunas_horas if c in df.columns]
    if cols_int:
        transformar_em_minutos(df , cols_int)
    df = padronizar_colunas_ponto(df)
    df = df.astype(object).where(pd.notna(df), None).replace('', None)
    try:
        pontos = df.to_dict(orient='records')
        return [Ponto(**row) for row in pontos] #type: ignore
    except Exception as e:
        raise ValueError(f'[!] Validação com Pydantic dos pontos falhou: {e}')

