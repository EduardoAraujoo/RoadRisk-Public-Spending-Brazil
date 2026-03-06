

import matplotlib.pyplot as plt
import seaborn as sns

def plot_annual_accidents(df, color_palette):
    """
    Gera um gráfico de barras com o volume total de acidentes por ano.
    """
    # Preparação dos dados para o gráfico
    annual_counts = df.groupby('year_reference').size()

    # Plotagem profissional com a identidade visual RoadRisk
    plt.figure(figsize=(12, 6))

    # Usando a cor primária da paleta
    ax = annual_counts.plot(kind='bar', color=color_palette[0], edgecolor='white', linewidth=1.2)

    # Refinamento Estético
    plt.title("Volume Total de Acidentes em MG por Ano (2017-2025)", 
              fontsize=14, pad=20, fontweight='bold', color=color_palette[0])
    plt.ylabel("Quantidade de Acidentes", fontsize=12, labelpad=10)
    plt.xlabel("Ano de Referência", fontsize=12, labelpad=10)
    plt.xticks(rotation=0) 
    plt.grid(axis='y', linestyle='--', alpha=0.4)

    # Adicionando Rótulos de Dados (Data Labels)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    fontsize=10, fontweight='bold', color=color_palette[0])

    # Finalização do Layout
    sns.despine()
    plt.tight_layout()
    plt.show()




def plot_annual_accidents(df, color_palette, color_idx=0):
    """
    Gera um gráfico de barras com o volume total de acidentes por ano.
    Permite escolher a cor da barra baseada na paleta do projeto.
    """
    annual_counts = df.groupby('year_reference').size()

    plt.figure(figsize=(12, 6))

    # Agora a cor da barra muda de acordo com o color_idx que passarmos!
    ax = annual_counts.plot(kind='bar', color=color_palette[color_idx], edgecolor='white', linewidth=1.2)

    # Estética RoadRisk
    plt.title("Volume Total de Acidentes em MG por Ano (2017-2025)", 
              fontsize=14, pad=20, fontweight='bold', color=color_palette[0])
    plt.ylabel("Quantidade de Acidentes", fontsize=12, labelpad=10)
    plt.xlabel("Ano de Referência", fontsize=12, labelpad=10)
    plt.xticks(rotation=0) 
    plt.grid(axis='y', linestyle='--', alpha=0.4)

    # Rótulos de dados
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    fontsize=10, fontweight='bold', color=color_palette[0])

    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_people_per_accident(df_pers, color_palette):
    """
    Calcula a densidade de pessoas por acidente, agrupa valores acima de 10 
    e gera um gráfico de barras focado na clareza visual.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 1. Cálculo da Densidade e Agrupamento
    pp_accident = df_pers.groupby('id').size().value_counts().sort_index()
    main_dist = pp_accident.iloc[:10].copy()
    main_dist['10+'] = pp_accident.iloc[10:].sum()

    # 2. Plotagem em Barras
    plt.figure(figsize=(12, 6))

    # Usando o Vibrant Orange (#FF851B / color_palette[1])
    ax = main_dist.plot(kind='bar', color=color_palette[1], edgecolor='white', linewidth=1.2)

    # Estética RoadRisk
    plt.title("Frequência de Acidentes por Número de Pessoas Envolvidas", 
              fontsize=14, pad=20, fontweight='bold', color=color_palette[0])
    plt.ylabel("Quantidade de Acidentes", fontsize=12)
    plt.xlabel("Número de Pessoas no Acidente", fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    # Adicionando rótulos de dados
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 10), 
                    textcoords='offset points', fontsize=9, fontweight='bold')

    sns.despine()
    plt.tight_layout()
    plt.show()

def plot_geographic_integrity(df_occ, color_palette):
    """
    Verifica se as coordenadas dos acidentes estão dentro dos limites 
    aproximados de Minas Gerais, gera um gráfico de validação e 
    retorna a taxa de validade dos dados.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 1. Definição dos limites aproximados de Minas Gerais
    lat_min, lat_max = -22.9, -14.2
    lon_min, lon_max = -51.1, -39.8

    # 2. Identificação de registros fora dos limites
    out_of_bounds = df_occ[
        (df_occ['latitude'] < lat_min) | (df_occ['latitude'] > lat_max) |
        (df_occ['longitude'] < lon_min) | (df_occ['longitude'] > lon_max)
    ]

    in_bounds_count = len(df_occ) - len(out_of_bounds)
    total_count = len(df_occ)
    validity_rate = (in_bounds_count / total_count) * 100

    # 3. Visualização de Integridade Geográfica
    plt.figure(figsize=(10, 5))
    labels = ['Dentro de MG', 'Fora dos Limites']
    values = [in_bounds_count, len(out_of_bounds)]
    
    # Cores: Navy Blue para os corretos e Soft Red (alerta) para os errados
    colors = [color_palette[0], color_palette[2]] 

    ax = plt.bar(labels, values, color=colors, edgecolor='white', linewidth=1.2)

    plt.title("Validação de Coordenadas: Acidentes dentro do Território de MG", 
              fontsize=14, pad=20, fontweight='bold', color=color_palette[0])
    plt.ylabel("Quantidade de Ocorrências")

    # Adicionando rótulos
    for p in ax:
        height = p.get_height()
        plt.annotate(f'{int(height)}\n({(height/total_count)*100:.1f}%)',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center', xytext=(0, 15), 
                    textcoords='offset points', fontsize=10, fontweight='bold')

    sns.despine()
    plt.tight_layout()
    plt.show()
    
    return validity_rate


def plot_max_km_per_br(df_occ, color_palette):
    """
    Identifica as 5 BRs com mais acidentes e plota o KM máximo registrado 
    para cada uma, servindo como auditoria de extensão das rodovias.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # 1. Seleção das 5 BRs com mais acidentes para auditoria
    top_brs = df_occ['br'].value_counts().head(5).index
    df_top_brs = df_occ[df_occ['br'].isin(top_brs)]

    # 2. Cálculo do KM Máximo registrado por BR
    max_km_per_br = df_top_brs.groupby('br')['km'].max().sort_values(ascending=False)

    # 3. Gráfico de Barras de Extensão Registrada
    plt.figure(figsize=(12, 6))
    # Usando o Vibrant Orange (color_palette[1])
    ax = max_km_per_br.plot(kind='bar', color=color_palette[1], edgecolor='white', linewidth=1.2)

    plt.title("Máximo KM Registrado por Rodovia (Top 5 BRs em MG)", 
              fontsize=14, pad=20, fontweight='bold', color=color_palette[0])
    plt.ylabel("Quilometragem (KM)")
    plt.xlabel("Rodovia Federal (BR)")
    plt.xticks(rotation=0)

    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())} km', 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), 
                    textcoords='offset points', fontsize=10, fontweight='bold')

    sns.despine()
    plt.tight_layout()
    plt.show()

def plot_severity_by_geo_availability(df_occ, color_palette):
    """
    Compara a gravidade média (mortos) entre acidentes que possuem 
    coordenadas GPS e os que não possuem (pontos cegos).
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # 1. Criar flag temporária para a análise
    # Usamos uma cópia para não alterar o dataframe original se não desejar
    df_temp = df_occ.copy()
    df_temp['has_geo'] = df_temp['latitude'].notnull() & df_temp['longitude'].notnull()

    # 2. Calcular gravidade média (Mortos)
    severity_comparison = df_temp.groupby('has_geo')['mortos'].mean()
    missing_gps_count = df_temp['has_geo'].value_counts().get(False, 0)

    # 3. Visualização
    plt.figure(figsize=(10, 5))
    # Cores: Red (color_palette[2]) para Sem GPS e Navy (color_palette[0]) para Com GPS
    ax = severity_comparison.plot(kind='bar', color=[color_palette[2], color_palette[0]], edgecolor='white')

    plt.title("Gravidade Média (Mortes): Com vs. Sem Localização GPS", 
              fontsize=14, pad=20, fontweight='bold', color=color_palette[0])
    plt.ylabel("Média de Mortos por Acidente")
    plt.xticks([0, 1], ['Sem GPS (Ponto Cego)', 'Com GPS'], rotation=0)

    sns.despine()
    plt.tight_layout()
    plt.show()

    return missing_gps_count