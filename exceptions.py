

class FileError(Exception):
    """Raised for errors related to file operations."""

    def __init__(self, fpath:str):
        super().__init__(f'file path: {fpath}')
