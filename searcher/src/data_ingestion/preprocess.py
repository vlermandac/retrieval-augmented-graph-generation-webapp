from typing import List
import logging
import fitz
import os
import re
from utils import doc_name_format
from core_classes import TextItem
from collections import Counter

logger = logging.getLogger(__name__)

new_doc_start = []
doc_names = []
new_page_start = []


def read_pdf(file_path):
    full_text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            lines = page.get_text().splitlines()
            for line in lines:
                if line.startswith('### DOC'):
                    doc_name = line.split(' ')[2].split('.')[0]
                    title = doc_name.split('-')[0]
                    author = doc_name.split('-')[1]
                    name = f"{author}. {title}"
                    doc_names.append(name.replace('_', ' '))
                    new_doc_start.append(len(full_text) + 1)
                    continue
                full_text += clean_text(line) + '\n'
            new_page_start.append(len(full_text) + 1)
    return full_text


def pdf_to_text(file_path: str) -> TextItem:
    filename = os.path.basename(file_path)
    logger.info(f"Reading {file_path}...")
    text = read_pdf(file_path)
    dir_name = os.path.dirname(file_path)
    words_freq_to_csv(text, dir_name)
    file_name = doc_name_format(filename, "author-title.type")
    document = TextItem(
        id=filename.split('.')[0],
        text=text,
        metadata=file_name.dict()
    )
    return document


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9áéíóúñ\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def lower_bound(lst, x):
    left, right = 0, len(lst) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if lst[mid] <= x:
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    return result


def chunking(doc: TextItem, size: int, overlap: int) -> List[TextItem]:
    chunks = []
    n = len(doc.text)
    for i, start in enumerate(range(0, n, size - overlap)):
        text = clean_text(doc.text[start:start + size])
        chunk = doc.create_child(new_id=str(i), new_text=text)
        start_page = lower_bound(new_page_start, start)
        end_page = lower_bound(new_page_start, min(start + size, n))
        current_doc = lower_bound(new_doc_start, start)
        chunk.metadata['start_page'] = start_page
        chunk.metadata['end_page'] = end_page
        chunk.metadata['doc_name'] = doc_names[current_doc]
        chunks.append(chunk)
    return chunks


def words_freq_to_csv(text: str, path: str) -> None:
    words = text.split()
    words_freq = Counter(words)
    file_name = os.path.join(path, 'words_freq.csv')
    with open(file_name, 'w') as f:
        f.write('word,frequency\n')
        for word, freq in words_freq.items():
            f.write(f'{word},{freq}\n')
