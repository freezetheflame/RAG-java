from app.db.doc_to_oss import DocToOSS
from data.build.pipeline import ProcessingPipeline


def main():
    pipeline = ProcessingPipeline()
    file_path = "data/阿里巴巴java开发手册.pdf"
    pipeline.process_document(file_path)
    ossloader = DocToOSS()
    ossloader.upload_file(file_path)
    print("successful")


if __name__ == '__main__':
    main()