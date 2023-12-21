from langchain_community.document_loaders.base import BaseLoader
from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredURLLoader,
    PyPDFLoader
)

LOADER_MAPPING = {
    "csv": (CSVLoader, {}),
    "doc": (UnstructuredWordDocumentLoader, {'mode': "elements"}),
    "docx": (UnstructuredWordDocumentLoader, {'mode': "elements"}),
    "enex": (EverNoteLoader, {}),
    "epub": (UnstructuredEPubLoader, {}),
    "html": (UnstructuredHTMLLoader, {}),
    "md": (UnstructuredMarkdownLoader, {}),
    "odt": (UnstructuredODTLoader, {}),
    "pdf": (PyPDFLoader, {}),
    "ppt": (UnstructuredPowerPointLoader, {'mode': "elements"}),
    "pptx": (UnstructuredPowerPointLoader, {'mode': "elements"}),
    "txt": (TextLoader, {"encoding": "utf8"}),
}


def get_loader(source: str) -> BaseLoader | None:
    """
    Get loader related to a source format
    :param source: source for recognition
    :return: loader
    """
    if source.lower().startswith('https://'):
        return UnstructuredURLLoader(urls=[source])

    mark = source.lower().split('.')[-1]
    if mark in LOADER_MAPPING:
        loader_cls, kwargs = LOADER_MAPPING[mark]
        return loader_cls(source, **kwargs)
