class PositionAnalysis:
    """
    Classe para análise de cargos.

    Esta classe fornece métodos para identificar os cargos únicos no conjunto de dados,
    calcular suas frequências e apresentar os resultados de forma ordenada.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações sobre cargos,
                               descrições e outras variáveis relevantes.
        """
        self.df = df

    def analyze_unique_positions(self, sort_by="Cargo", ascending=True):
        """
        Analisa os cargos únicos no conjunto de dados e calcula suas frequências.

        Este método conta o número de ocorrências de cada cargo na coluna `cbo_2002_descricao`,
        retorna o total de cargos diferentes e um DataFrame com os nomes e frequências dos cargos,
        ordenados de acordo com os parâmetros especificados.

        Parameters:
            sort_by (str): A coluna usada para ordenar os resultados.
                           Valores possíveis:
                           - "Cargo": Ordena alfabeticamente pelo nome do cargo.
                           - "Frequência": Ordena pela frequência dos cargos.
            ascending (bool): Define se a ordenação será crescente (True) ou decrescente (False).
                              Exemplo: Para listar os cargos mais frequentes primeiro, use
                              `sort_by="Frequência"` e `ascending=False`.

        Returns:
            dict: Um dicionário contendo:
                - "Total de Cargos Diferentes": O número total de cargos únicos.
                - "Cargos": Um DataFrame com os nomes dos cargos e suas respectivas frequências,
                            ordenados de acordo com os parâmetros fornecidos.

        Exemplo de Uso:
            Para analisar os cargos únicos e ordená-los pela frequência em ordem decrescente:
                analyze_unique_positions(sort_by="Frequência", ascending=False)
        """
        # Conta o número de ocorrências de cada cargo
        position_counts = self.df['cbo_2002_descricao'].value_counts().reset_index()

        # Renomeia as colunas para "Cargo" e "Frequência"
        position_counts.columns = ['Cargo', 'Frequência']

        # Ordena os cargos pelo critério especificado
        position_counts = position_counts.sort_values(by=sort_by, ascending=ascending)

        return {
            "Total de Cargos Diferentes": len(position_counts),
            "Cargos": position_counts
        }
