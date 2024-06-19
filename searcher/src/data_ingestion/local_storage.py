import os
import shutil
from fastapi import UploadFile
from utils import doc_name_format


def create_storage_path(filename: str, from_dir: str) -> str:
    file_title = doc_name_format(filename).title
    dir_path = os.path.join(from_dir, file_title)
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, filename)


def save_file(file: UploadFile, path: str) -> str:
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path


def delete_dir(path: str):
    shutil.rmtree(path)
