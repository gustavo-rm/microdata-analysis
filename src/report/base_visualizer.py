import os
import matplotlib.pyplot as plt

class BaseVisualizer:
    """
    Classe base para visualizadores, fornecendo funcionalidades comuns para salvar gráficos.
    """

    def __init__(self, output_dir="output"):
        """
        Inicializa a classe base com um diretório de saída.

        Parameters:
            output_dir (str): Diretório onde os gráficos serão salvos.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_plot(self, filename):
        """
        Salva o gráfico atual no diretório especificado.

        Parameters:
            filename (str): Nome do arquivo onde o gráfico será salvo.
        """
        plt.savefig(os.path.join(self.output_dir, filename), format="png", dpi=300)
        plt.close()  # Fecha o gráfico para liberar memória
