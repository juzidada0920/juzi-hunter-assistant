"""文件处理工具 —— 支持 PDF / Word / TXT 文本提取"""

import io

import fitz  # PyMuPDF
from docx import Document


def read_pdf(file_like) -> str:
    """从 PDF 文件中提取文本。

    Args:
        file_like: 文件路径 (str) 或 BytesIO 对象

    Returns:
        str: 提取的全部文本
    """
    doc = fitz.open(file_like)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    doc.close()
    return "\n".join(texts)


def read_docx(file_like) -> str:
    """从 Word 文件中提取文本。

    Args:
        file_like: 文件路径 (str) 或 BytesIO 对象

    Returns:
        str: 提取的全部文本
    """
    doc = Document(file_like)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_text_from_upload(uploaded_file) -> str:
    """根据文件扩展名自动选择提取方式。

    Args:
        uploaded_file: Streamlit UploadedFile 对象

    Returns:
        str: 提取的全部文本
    """
    filename = uploaded_file.name.lower()
    file_bytes = io.BytesIO(uploaded_file.read())

    if filename.endswith(".pdf"):
        return read_pdf(file_bytes)
    elif filename.endswith((".docx", ".doc")):
        return read_docx(file_bytes)
    elif filename.endswith(".txt"):
        return file_bytes.read().decode("utf-8", errors="replace")
    else:
        # 尝试当纯文本读
        return file_bytes.read().decode("utf-8", errors="replace")
