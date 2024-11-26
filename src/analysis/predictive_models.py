from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class PredictiveModels:
    """
    Classe para criação e avaliação de modelos preditivos.

    Esta classe fornece métodos para executar modelos de Regressão Linear
    e Regressão Logística, usados para prever valores numéricos e probabilidades,
    respectivamente.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo as variáveis independentes e dependentes
                               para treinar e avaliar os modelos preditivos.
        """
        self.df = df

    def linear_regression_salary(self):
        """
        Executa Regressão Linear para prever salários com base em idade, tempo de emprego
        e grau de instrução.

        Este método treina um modelo de Regressão Linear para estimar a variável
        dependente `valor_remuneracao_media` usando as variáveis independentes
        `idade`, `tempo_emprego` e `grau_instrucao_apos_2005` (convertida para valores numéricos).

        Returns:
            dict: Contém os resultados do modelo, incluindo:
                - "Coeficientes": Um dicionário mapeando cada variável independente para seu coeficiente.
                - "Intercepto": O valor do intercepto da regressão.
                - "R²": O coeficiente de determinação (indicador de ajuste do modelo).
                - "Erro Quadrático Médio": Mede o erro médio das previsões.

        Exemplo de Uso:
            Use este método para prever salários em um conjunto de dados com variáveis
            como idade e tempo de emprego:
                results = linear_regression_salary()
                print(results['R²'], results['Erro Quadrático Médio'])
        """
        # Define as variáveis independentes
        features = ['idade', 'tempo_emprego']

        # Adiciona grau de instrução como variável numérica, se disponível
        if 'grau_instrucao_apos_2005' in self.df.columns:
            self.df['grau_instrucao_num'] = self.df['grau_instrucao_apos_2005'].factorize()[0]
            features.append('grau_instrucao_num')

        # Remove valores nulos das colunas relevantes
        df_clean = self.df.dropna(subset=features + ['valor_remuneracao_media'])

        # Define X (variáveis independentes) e y (variável dependente)
        X = df_clean[features]
        y = df_clean['valor_remuneracao_media']

        # Divide os dados em conjuntos de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treina o modelo de Regressão Linear
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Retorna os resultados
        return {
            "Coeficientes": dict(zip(features, model.coef_)),
            "Intercepto": model.intercept_,
            "R²": model.score(X_test, y_test),
            "Erro Quadrático Médio": mean_squared_error(y_test, model.predict(X_test))
        }

    def logistic_regression_active_link(self):
        """
        Executa Regressão Logística para prever a probabilidade de vínculos ativos
        com base em idade, gênero e região.

        Este método treina um modelo de Regressão Logística para prever a variável
        dependente `vinculo_ativo_3112` (convertida para binária: "Sim" -> 1, "Não" -> 0)
        usando variáveis independentes como `idade`, `sigla_uf` e `sexo` (convertido para numérico).

        Returns:
            dict: Contém as métricas de avaliação do modelo:
                - "Acurácia": Proporção de previsões corretas.
                - "Relatório de Classificação": Métricas detalhadas (precisão, recall, F1-score)
                  para cada classe (ativo ou inativo).

        Exemplo de Uso:
            Use este método para prever vínculos ativos:
                results = logistic_regression_active_link()
                print(results['Acurácia'])
                print(results['Relatório de Classificação'])
        """
        # Define as variáveis independentes
        features = ['idade', 'sigla_uf', 'sexo']

        # Remove valores nulos das colunas relevantes
        df_clean = self.df.dropna(subset=features + ['vinculo_ativo_3112'])

        # Define X (variáveis independentes) e y (variável dependente)
        X = df_clean[features]
        y = df_clean['vinculo_ativo_3112'].apply(lambda x: 1 if x == "Sim" else 0)  # Binário

        # Converter variáveis categóricas para numéricas
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(drop='first'), ['sigla_uf', 'sexo']),
                ('num', 'passthrough', ['idade']),
            ]
        )

        # Criar o pipeline com o modelo
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(max_iter=1000))
        ])

        # Dividir os dados em conjuntos de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treinar o modelo
        model.fit(X_train, y_train)

        # Retorna as métricas de avaliação
        predictions = model.predict(X_test)
        return {
            "Acurácia": accuracy_score(y_test, predictions),
            "Relatório de Classificação": classification_report(y_test, predictions, output_dict=True)
        }
