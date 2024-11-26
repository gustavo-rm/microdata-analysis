import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from src.report.base_visualizer import BaseVisualizer
from src.analysis.predictive_models import PredictiveModels

class PredictiveModelsVisualizer(BaseVisualizer):
    """
    Classe para gerar visualizações dos modelos preditivos.
    """

    def __init__(self, df, output_dir="output"):
        """
        Inicializa a instância com um DataFrame e o diretório de saída para salvar os gráficos.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo as variáveis independentes e dependentes.
            output_dir (str): O diretório onde os gráficos serão salvos.
        """
        super().__init__(output_dir)  # Herda o construtor da classe BaseVisualizer
        self.models = PredictiveModels(df)  # Instancia PredictiveModels com o DataFrame

    def plot_linear_regression_coefficients(self):
        """
        Gera um gráfico de barras mostrando os coeficientes do modelo de Regressão Linear.
        """
        results = self.models.linear_regression_salary()
        coefficients = results["Coeficientes"]

        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(coefficients.keys()), y=list(coefficients.values()), palette="Blues")
        plt.title("Coeficientes da Regressão Linear")
        plt.ylabel("Coeficiente")
        plt.xlabel("Variáveis Independentes")
        plt.tight_layout()

        self.save_plot("linear_regression_coefficients.png")

    def plot_logistic_regression_classification_report(self):
        """
        Gera um gráfico de barras para o relatório de classificação do modelo de Regressão Logística.
        """
        results = self.models.logistic_regression_active_link()
        report = results["Relatório de Classificação"]

        # Transformar o relatório em um DataFrame para visualização
        report_df = pd.DataFrame(report).T
        report_df = report_df.loc[['0', '1', 'accuracy']]  # Foco em classes e acurácia
        metrics = ['precision', 'recall', 'f1-score']

        plt.figure(figsize=(12, 6))
        report_df[metrics].plot(kind='bar', figsize=(12, 6), colormap='coolwarm')
        plt.title("Relatório de Classificação - Regressão Logística")
        plt.ylabel("Pontuação")
        plt.xlabel("Classe / Métrica")
        plt.xticks(rotation=0)
        plt.legend(title="Métricas")
        plt.tight_layout()

        self.save_plot("logistic_regression_classification_report.png")

    def plot_linear_regression_predictions(self):
        """
        Gera um gráfico de dispersão comparando valores reais e preditos pela Regressão Linear.
        """
        # Reexecutar o modelo para capturar os conjuntos de dados
        features = ['idade', 'tempo_emprego']
        if 'grau_instrucao_apos_2005' in self.models.df.columns:
            self.models.df['grau_instrucao_num'] = self.models.df['grau_instrucao_apos_2005'].factorize()[0]
            features.append('grau_instrucao_num')

        df_clean = self.models.df.dropna(subset=features + ['valor_remuneracao_media'])
        X = df_clean[features]
        y = df_clean['valor_remuneracao_media']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        # Plotar valores reais vs preditos
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.6, edgecolors='k', label="Predições")
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label="Ideal")
        plt.title("Valores Reais vs Preditos - Regressão Linear")
        plt.xlabel("Valores Reais")
        plt.ylabel("Valores Preditos")
        plt.legend()
        plt.tight_layout()

        self.save_plot("linear_regression_predictions.png")
