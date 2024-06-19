from typing import List
import logging
import fitz
import os
import re
from utils import doc_name_format
from core_classes import TextItem

logger = logging.getLogger(__name__)


def pdf_to_text(file_path: str) -> TextItem:
    filename = os.path.basename(file_path)
    logger.info(f"Reading {file_path}...")
    with fitz.open(file_path) as doc:
        text = '\n'.join(page.get_text() for page in doc)
    file_name = doc_name_format(filename, "author-title.type")
    document = TextItem(
        id=filename.split('.')[0],
        text=text,
        metadata=file_name.dict()
    )
    return document


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def chunking(doc: TextItem, size: int, overlap: int) -> List[TextItem]:
    chunks = []
    n = len(doc.text)
    for i, start in enumerate(range(0, n, size - overlap)):
        text = clean_text(doc.text[start:start + size])
        chunk = doc.create_child(new_id=str(i), new_text=text)
        chunks.append(chunk)
    return chunks
