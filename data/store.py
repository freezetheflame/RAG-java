from app.db.doc_to_oss import DocToOSS
from data.build.pipeline import ProcessingPipeline


def main():
    pipeline = ProcessingPipeline()
    file_path = "./data/JVM.pdf"
    pipeline.process_document(file_path)
    ossloader = DocToOSS()
    ossloader.upload_file(file_path)
    print("successful")


if __name__ == '__main__':
    main()