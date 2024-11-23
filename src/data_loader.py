import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Carrega os dados do arquivo e retorna um DataFrame."""
        return pd.read_csv(self.file_path)

    def preprocess_data(self, df):
        """Realiza limpeza e transformação básica nos dados."""
        df = df.dropna()  # Exemplo: remove linhas com valores nulos
        return df
