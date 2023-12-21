import importlib
import os
from typing import List, Any

from chainlit import message


def load_object(obj_path: str, default_obj_path: str = '') -> Any:
    obj_path_list = obj_path.rsplit('.', 1)
    obj_path = obj_path_list.pop(0) if len(obj_path_list) > 1 else default_obj_path
    obj_name = obj_path_list[0]
    module_obj = importlib.import_module(obj_path)
    if not hasattr(module_obj, obj_name):  # noqa: WPS421
        raise AttributeError(f'Object `{obj_name}` cannot be loaded from `{obj_path}`.')
    return getattr(module_obj, obj_name)


def check_and_write_files(_message: message.Message) -> List[str]:
    files = []
    for item in _message.elements:
        files.append(item.name)
        write_file(item.name, item.content)
    return files


def write_file(path: str, content: bytes, rewrite: bool = False):
    if not os.path.exists(path) or rewrite:
        with open(path, 'wb') as file_:
            file_.write(content)
