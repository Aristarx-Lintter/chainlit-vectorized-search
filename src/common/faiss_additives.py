from os.path import basename
from typing import List, Union

from langchain_community.vectorstores.faiss import FAISS


def get_sources(index: FAISS, raw: bool = True) -> List[str]:
    """
    Get list of sources
    :param index:
    :param raw:
    :return:
    """
    sources = []
    for item in index.docstore._dict:
        meta = index.docstore._dict[item].metadata
        if "source" in meta:
            if not meta["source"] in sources:
                sources.append(meta["source"])

    sources = sources if raw else [basename(source) for source in sources]
    return sources


def match_sources(sources: List[str], index: FAISS):
    matched_keys = []

    for item in index.docstore._dict:
        meta = index.docstore._dict[item].metadata
        if "source" in meta:
            if meta["source"] in sources or basename(meta["source"]) in sources:
                matched_keys.append(item)
    return matched_keys


def concatenate_indexes(
        vectorstore: FAISS, embeddings, path: str,
) -> Union[FAISS, None]:
    """
    Concatenate vectorstore and existing indexes
    :param vectorstore: vectorstore for concatenation
    :param embeddings: model to vectorize the information
    :param path: path to the existing index
    :return: new vectorstore and list of existing sources
    """
    try:
        faiss_index = FAISS.load_local(path, embeddings)
    except Exception as e:
        print("Vector base with path {} does not exist".format(path))
        print(e)
        return None

    if not vectorstore:
        vectorstore = faiss_index
    else:
        existing_sources = get_sources(vectorstore)
        matched_items = match_sources(existing_sources, faiss_index)
        if matched_items:
            faiss_index.delete(matched_items)
        vectorstore.merge_from(faiss_index)

    return vectorstore
