import pandas as pd


class DataLoader:
    """
    Classe responsável por carregar, limpar e pré-processar os dados de um arquivo CSV.
    """

    def __init__(self, file_path):
        """
        Inicializa a instância da classe com o caminho do arquivo.

        Parameters:
            file_path (str): Caminho para o arquivo CSV.
        """
        self.file_path = file_path

    def load_data(self):
        """
        Carrega os dados do arquivo CSV e retorna um DataFrame.

        Returns:
            pd.DataFrame: Dados carregados em um DataFrame do Pandas.
        """
        return pd.read_csv(self.file_path, low_memory=False)

    def preprocess_data(self, df):
        """
        Realiza pré-processamento básico e avançado nos dados.

        Inclui:
        - Limpeza de valores ausentes e inconsistentes.
        - Conversão de tipos de dados.
        - Remoção de outliers na média salarial.
        - Padronização de colunas.

        Parameters:
            df (pd.DataFrame): O DataFrame carregado com os dados brutos.

        Returns:
            pd.DataFrame: Dados limpos e pré-processados.
        """
        # 1. Substituir valores nulos em colunas categóricas
        df['tipo_salario'] = df['tipo_salario'].fillna("Desconhecido").astype(str)
        df['sigla_uf_nome'] = df['sigla_uf_nome'].fillna("Desconhecido")
        df['tipo_vinculo'] = df['tipo_vinculo'].fillna("Não Informado")

        # 2. Remover linhas com valores críticos ausentes
        required_columns = ['cbo_2002', 'valor_remuneracao_media', 'idade', 'sigla_uf']
        df = df.dropna(subset=required_columns)

        # 3. Converter colunas numéricas para os tipos corretos
        numeric_columns = ['valor_remuneracao_media', 'idade', 'tempo_emprego']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 4. Padronizar colunas categóricas
        if 'sexo' in df.columns:
            df['sexo'] = df['sexo'].str.title()  # Exemplo: "masculino" -> "Masculino"

        # 5. Filtrar registros com valores fora dos limites aceitáveis
        df = df[(df['idade'] >= 18) & (df['idade'] <= 64)]  # Faixa etária válida

        # 6. Remover outliers na média salarial usando IQR
        df = self.remove_outliers(df, 'valor_remuneracao_media')

        # 7. Garantir que não haja valores duplicados desnecessários
        df = df.drop_duplicates()

        return df

    @staticmethod
    def remove_outliers(df, column):
        """
        Remove outliers de uma coluna numérica usando o método do intervalo interquartil (IQR).

        Parameters:
            df (pd.DataFrame): O DataFrame original.
            column (str): Nome da coluna onde os outliers serão removidos.

        Returns:
            pd.DataFrame: DataFrame sem os outliers na coluna especificada.
        """
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filtrar valores dentro do intervalo interquartil
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
