from src.data.data_loader import DataLoader
from src.config import Config
from src.report.report_generator import ReportGenerator


def main():
    # 1. Carregar e preprocessar os dados
    # Caminho do arquivo CSV
    file_path = Config.RAW_DATA_PATH + "microdados.csv"
    loader = DataLoader(file_path)
    data = loader.load_data()
    data = loader.preprocess_data(data)

    # Criar o gerador de relatórios
    report_gen = ReportGenerator(data, output_dir="output")

    # Gerar todos os relatórios
    report_gen.generate_all_reports()

if __name__ == "__main__":
    main()
