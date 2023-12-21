from typing import List

from chainlit.types import AskFileResponse


class Postprocessing:
    def __init__(self, write_files: callable, process_files: callable) -> None:
        self.write_files = write_files
        self.process_files = process_files

    def __call__(self, files: List[AskFileResponse]) -> None:
        for file_ in files:
            self.write_files(file_.path, file_.content)

        self.process_files([file_.path for file_ in files])
