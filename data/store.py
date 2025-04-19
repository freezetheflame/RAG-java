from app.db.doc_to_oss import DocToOSS
from data.build.pipeline import ProcessingPipeline


def main():
    pipeline = ProcessingPipeline()
    file_path = "./source/Java程序员面试宝典.pdf"
    pipeline.process_document(file_path)
    # ossLoader = DocToOSS()
    # ossLoader.upload_file(file_path)
    print("successful")


if __name__ == '__main__':
    main()