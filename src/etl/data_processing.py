# Arquivo: src/etl/data_processing.py
import pandas as pd

def generate_dtypes_audit(df):
    """
    Gera um DataFrame de auditoria com os tipos de dados, 
    quantidade de valores únicos e um exemplo prático de cada coluna.
    """
    audit_df = pd.DataFrame({
        'Dtype Atual': df.dtypes,
        'Valores Únicos': df.nunique(),
        'Exemplo': df.iloc[0]
    })
    
    return audit_df


def calculate_match_rate(df_occ, df_pers):
    """
    Calcula a taxa de integridade (match rate) entre as tabelas 
    de ocorrências (df_occ) e pessoas envolvidas (df_pers).
    """
    ids_occ = set(df_occ['id'].unique())
    ids_pers = set(df_pers['id'].unique())
    
    # Calcula a interseção dividida pelo total de pessoas
    match_rate = (len(ids_pers & ids_occ) / len(ids_pers)) * 100
    
    return match_rate

# Adicione ao final do arquivo: src/etl/data_processing.py


# Arquivo: src/etl/data_processing.py
import pandas as pd

def apply_business_intelligence(df):
    """
    Versão Blindada: Aplica as regras de negócio (EOC, horários e causas).
    As funções auxiliares estão internas para evitar erros de escopo no Jupyter.
    """
    
    # --- DEFINIÇÃO DAS FUNÇÕES INTERNAS (NÃO MEXER) ---
    def _calc_eoc(row):
        custo_base = 3500.00 
        p_fatal, p_grave, p_leve = 665000.0, 145000.0, 25000.0
        return custo_base + (row['mortos'] * p_fatal) + (row['feridos_graves'] * p_grave) + (row['feridos_leves'] * p_leve)

    def _get_periodo(hora_str):
        try:
            h = int(str(hora_str).split(':')[0])
            if 0 <= h < 6: return 'Madrugada'
            if 6 <= h < 12: return 'Manhã'
            if 12 <= h < 18: return 'Tarde'
            return 'Noite'
        except: return 'Não Identificado'

    def _get_causa_grupo(causa):
        c = str(causa).lower()
        if any(x in c for x in ['falta', 'atenção', 'álcool', 'velocidade', 'dormindo', 'desobediência']): return 'Fator Humano'
        if any(x in c for x in ['pista', 'escorregadia', 'neblina', 'defeito', 'animal', 'sinalização']): return 'Fator Via/Clima'
        return 'Outros/Mecânico'

    # --- EXECUÇÃO DA LÓGICA ---
    df = df.copy() # Garante que não alteramos o original por acidente
    
    col_causa = 'causa_acidente' if 'causa_acidente' in df.columns else 'causa_principal'

    df['eoc_estimado'] = df.apply(_calc_eoc, axis=1)
    df['periodo_dia'] = df['horario'].apply(_get_periodo)
    df['tipo_causa_grupo'] = df[col_causa].apply(_get_causa_grupo)
    
    return df, col_causa