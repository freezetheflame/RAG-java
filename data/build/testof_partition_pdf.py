from PyPDF2 import PdfReader
from unstructured.partition.pdf import partition_pdf

file_path = "../data/ComputerArchitecture.pdf"

def main():
    # 读取PDF文件
    elements = partition_pdf(
                filename="../data/ComputerArchitecture.pdf",
                strategy="fast",  # fast
                extract_images_in_pdf=False,
                infer_table_structure=True,
                include_page_breaks=True,
            )
    # 将元素转换为文本
    print(elements)
    text = "\n".join([element.text for element in elements])
    # 打印文本内容
    print(text)
    print("end")

def hard_read():
    reader = PdfReader(file_path)
    elements = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            elements.append(text)
    print(elements)

if __name__ == "__main__":
    hard_read()