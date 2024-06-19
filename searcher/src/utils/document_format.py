from pydantic import BaseModel
import re


class DocName(BaseModel):
    author: str
    title: str
    file_type: str


def doc_name_format(name: str, format: str = 'author-title.type') -> DocName:
    name = name.split('/')[-1].lower()
    ext = name.split('.')[-1].lower()
    name = name.split('.')[0]
    if (format != 'author-title.type') or not bool(re.match(r'^[^-]+-[^-]+$', name)):
        return DocName(
            author="unknown",
            title=name,
            file_type=ext
        )

    return DocName(
        author=name.split('-')[0],
        title=name.split('-')[1],
        file_type=ext
    )
