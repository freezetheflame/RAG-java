from data.build.pipeline import ProcessingPipeline


def main():
    pipeline = ProcessingPipeline()
    file_path = "data/分布式面试资料.pdf"
    pipeline.process_document(file_path)
    print("successful")


if __name__ == '__main__':
    main()