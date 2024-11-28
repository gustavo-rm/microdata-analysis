from src.data.data_loader import DataLoader
from src.config import Config
from src.report.report_generator import ReportGenerator
from src.report.analysis_to_document import AnalysisToDocument


def main():
    # Caminho do arquivo CSV
    file_path = Config.RAW_DATA_PATH + "microdados.csv"

    # Carregar e preprocessar os dados (Total: 741437)
    loader = DataLoader(file_path)
    data = loader.load_data()
    data = loader.preprocess_data(data)

    # Criar o documento com os dados
    analysis_doc = AnalysisToDocument(data)
    analysis_doc.run_analysis()

    # Criar o gerador de relatórios
    report_gen = ReportGenerator(data, output_dir="output")

    # Gerar todos os gráficos
    report_gen.generate_all_reports()

if __name__ == "__main__":
    main()
