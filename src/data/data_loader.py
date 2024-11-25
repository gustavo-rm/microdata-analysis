import pandas as pd


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Carrega os dados do arquivo CSV e retorna um DataFrame."""
        return pd.read_csv(self.file_path)

    def preprocess_data(self, df):
        """Realiza limpeza e transformação básica nos dados."""
        # Remove linhas com valores críticos ausentes
        df = df.dropna(subset=['cbo_2002', 'valor_remuneracao_media', 'idade', 'sigla_uf'])

        # Converte colunas numéricas para os tipos corretos
        df['valor_remuneracao_media'] = pd.to_numeric(df['valor_remuneracao_media'], errors='coerce')
        df['idade'] = pd.to_numeric(df['idade'], errors='coerce')

        # Preenchendo valores nulos com padrões para evitar erros futuros
        df = df.fillna({'sigla_uf_nome': 'Desconhecido', 'tipo_vinculo': 'Não Informado'})

        return df

